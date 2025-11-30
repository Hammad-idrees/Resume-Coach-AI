import { Router, Request, Response } from 'express';
import { supabase } from '../config/supabase';

const router = Router();

// GET /api/resumes - Get all resumes for authenticated user
router.get('/', async (req: Request, res: Response) => {
  try {
    const userId = req.headers['x-user-id'] as string;
    
    if (!userId) {
      return res.status(401).json({ error: 'User ID required in headers' });
    }

    const { data, error } = await supabase
      .from('resumes')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });

    if (error) throw error;

    res.json({ resumes: data || [], count: data?.length || 0 });
  } catch (error: any) {
    console.error('Error fetching resumes:', error);
    res.status(500).json({ error: 'Failed to fetch resumes', message: error.message });
  }
});

// GET /api/resumes/:id - Get single resume by ID
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const userId = req.headers['x-user-id'] as string;

    if (!userId) {
      return res.status(401).json({ error: 'User ID required in headers' });
    }

    const { data, error } = await supabase
      .from('resumes')
      .select('*')
      .eq('id', id)
      .eq('user_id', userId)
      .single();

    if (error) throw error;

    if (!data) {
      return res.status(404).json({ error: 'Resume not found' });
    }

    res.json({ resume: data });
  } catch (error: any) {
    console.error('Error fetching resume:', error);
    res.status(500).json({ error: 'Failed to fetch resume', message: error.message });
  }
});

// POST /api/resumes - Create new resume
router.post('/', async (req: Request, res: Response) => {
  try {
    const userId = req.headers['x-user-id'] as string;
    
    if (!userId) {
      return res.status(401).json({ error: 'User ID required in headers' });
    }

    const { title, content, skills, experience, education } = req.body;

    if (!title || !content) {
      return res.status(400).json({ error: 'Title and content are required' });
    }

    const { data, error } = await supabase
      .from('resumes')
      .insert([{
        user_id: userId,
        title,
        content,
        skills: skills || [],
        experience: experience || [],
        education: education || []
      }])
      .select()
      .single();

    if (error) throw error;

    res.status(201).json({ 
      message: 'Resume created successfully',
      resume: data 
    });
  } catch (error: any) {
    console.error('Error creating resume:', error);
    res.status(500).json({ error: 'Failed to create resume', message: error.message });
  }
});

// PUT /api/resumes/:id - Update resume
router.put('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const userId = req.headers['x-user-id'] as string;

    if (!userId) {
      return res.status(401).json({ error: 'User ID required in headers' });
    }

    const { title, content, skills, experience, education } = req.body;

    const updateData: any = {};
    if (title !== undefined) updateData.title = title;
    if (content !== undefined) updateData.content = content;
    if (skills !== undefined) updateData.skills = skills;
    if (experience !== undefined) updateData.experience = experience;
    if (education !== undefined) updateData.education = education;

    const { data, error } = await supabase
      .from('resumes')
      .update(updateData)
      .eq('id', id)
      .eq('user_id', userId)
      .select()
      .single();

    if (error) throw error;

    if (!data) {
      return res.status(404).json({ error: 'Resume not found' });
    }

    res.json({ 
      message: 'Resume updated successfully',
      resume: data 
    });
  } catch (error: any) {
    console.error('Error updating resume:', error);
    res.status(500).json({ error: 'Failed to update resume', message: error.message });
  }
});

// DELETE /api/resumes/:id - Delete resume
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const userId = req.headers['x-user-id'] as string;

    if (!userId) {
      return res.status(401).json({ error: 'User ID required in headers' });
    }

    const { error } = await supabase
      .from('resumes')
      .delete()
      .eq('id', id)
      .eq('user_id', userId);

    if (error) throw error;

    res.json({ message: 'Resume deleted successfully' });
  } catch (error: any) {
    console.error('Error deleting resume:', error);
    res.status(500).json({ error: 'Failed to delete resume', message: error.message });
  }
});

export default router;
