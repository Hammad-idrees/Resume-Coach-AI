import { Router, Request, Response } from 'express';
import axios from 'axios';
import { supabase } from '../config/supabase';

const router = Router();

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';

// POST /api/score - Get match score for resume and job
router.post('/', async (req: Request, res: Response) => {
  try {
    const { resume_text, job_description, resume_id, job_id, user_id } = req.body;

    if (!resume_text || !job_description) {
      return res.status(400).json({ 
        error: 'Both resume_text and job_description are required' 
      });
    }

    // Call ML service for prediction
    console.log(`Calling ML service at ${ML_SERVICE_URL}/predict-match`);
    
    const mlResponse = await axios.post(`${ML_SERVICE_URL}/predict-match`, {
      resume_text,
      job_description
    }, {
      timeout: 10000 // 10 second timeout
    });

    const scoreData = mlResponse.data;

    // Optionally save score to database if resume_id and job_id provided
    if (resume_id && job_id && user_id) {
      const { data: savedScore, error: dbError } = await supabase
        .from('scores')
        .insert([{
          user_id,
          resume_id,
          job_id,
          match_score: scoreData.match_score,
          confidence: scoreData.confidence,
          keywords_matched: scoreData.keywords_matched,
          recommendation: scoreData.recommendation
        }])
        .select()
        .single();

      if (dbError) {
        console.error('Error saving score to database:', dbError);
        // Don't fail the request, just log the error
      } else {
        console.log('Score saved to database:', savedScore.id);
      }
    }

    res.json({
      success: true,
      score: scoreData
    });

  } catch (error: any) {
    console.error('Error getting match score:', error);
    
    if (error.code === 'ECONNREFUSED') {
      return res.status(503).json({ 
        error: 'ML service unavailable',
        message: 'Could not connect to ML service. Please ensure it is running.',
        ml_service_url: ML_SERVICE_URL
      });
    }

    if (error.response) {
      return res.status(error.response.status).json({
        error: 'ML service error',
        message: error.response.data
      });
    }

    res.status(500).json({ 
      error: 'Failed to get match score',
      message: error.message 
    });
  }
});

// GET /api/score/history - Get user's score history
router.get('/history', async (req: Request, res: Response) => {
  try {
    const userId = req.headers['x-user-id'] as string;
    
    if (!userId) {
      return res.status(401).json({ error: 'User ID required in headers' });
    }

    const { data, error } = await supabase
      .from('scores')
      .select(`
        *,
        resumes:resume_id(id, title),
        jobs:job_id(id, title, company)
      `)
      .eq('user_id', userId)
      .order('created_at', { ascending: false });

    if (error) throw error;

    res.json({ 
      scores: data || [],
      count: data?.length || 0 
    });
  } catch (error: any) {
    console.error('Error fetching score history:', error);
    res.status(500).json({ 
      error: 'Failed to fetch score history',
      message: error.message 
    });
  }
});

// GET /api/score/:id - Get single score by ID
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const userId = req.headers['x-user-id'] as string;

    if (!userId) {
      return res.status(401).json({ error: 'User ID required in headers' });
    }

    const { data, error } = await supabase
      .from('scores')
      .select(`
        *,
        resumes:resume_id(id, title, content),
        jobs:job_id(id, title, company, description)
      `)
      .eq('id', id)
      .eq('user_id', userId)
      .single();

    if (error) throw error;

    if (!data) {
      return res.status(404).json({ error: 'Score not found' });
    }

    res.json({ score: data });
  } catch (error: any) {
    console.error('Error fetching score:', error);
    res.status(500).json({ 
      error: 'Failed to fetch score',
      message: error.message 
    });
  }
});

// GET /api/score/ml/health - Check ML service health
router.get('/ml/health', async (req: Request, res: Response) => {
  try {
    const healthResponse = await axios.get(`${ML_SERVICE_URL}/health`, {
      timeout: 5000
    });

    res.json({
      ml_service: 'available',
      ml_service_url: ML_SERVICE_URL,
      health: healthResponse.data
    });
  } catch (error: any) {
    console.error('ML service health check failed:', error.message);
    res.status(503).json({
      ml_service: 'unavailable',
      ml_service_url: ML_SERVICE_URL,
      error: error.message
    });
  }
});

export default router;
