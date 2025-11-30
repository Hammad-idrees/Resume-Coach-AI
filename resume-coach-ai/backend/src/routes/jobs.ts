import { Router, Request, Response } from 'express';
import { supabase } from '../config/supabase';

const router = Router();

// GET /api/jobs - Get all job postings
router.get('/', async (req: Request, res: Response) => {
  try {
    const { data, error } = await supabase
      .from('jobs')
      .select('*')
      .order('created_at', { ascending: false });

    if (error) throw error;

    res.json({ jobs: data || [], count: data?.length || 0 });
  } catch (error: any) {
    console.error('Error fetching jobs:', error);
    res.status(500).json({ error: 'Failed to fetch jobs', message: error.message });
  }
});

// GET /api/jobs/:id - Get single job by ID
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const { data, error } = await supabase
      .from('jobs')
      .select('*')
      .eq('id', id)
      .single();

    if (error) throw error;

    if (!data) {
      return res.status(404).json({ error: 'Job not found' });
    }

    res.json({ job: data });
  } catch (error: any) {
    console.error('Error fetching job:', error);
    res.status(500).json({ error: 'Failed to fetch job', message: error.message });
  }
});

// POST /api/jobs - Create new job posting (admin only)
router.post('/', async (req: Request, res: Response) => {
  try {
    const { title, description, company, location, salary, requirements, skills } = req.body;

    if (!title || !description || !company) {
      return res.status(400).json({ error: 'Title, description, and company are required' });
    }

    const { data, error } = await supabase
      .from('jobs')
      .insert([{
        title,
        description,
        company,
        location: location || 'Remote',
        salary: salary || 'Competitive',
        requirements: requirements || [],
        skills: skills || []
      }])
      .select()
      .single();

    if (error) throw error;

    res.status(201).json({ 
      message: 'Job created successfully',
      job: data 
    });
  } catch (error: any) {
    console.error('Error creating job:', error);
    res.status(500).json({ error: 'Failed to create job', message: error.message });
  }
});

// PUT /api/jobs/:id - Update job posting (admin only)
router.put('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const { title, description, company, location, salary, requirements, skills } = req.body;

    const updateData: any = {};
    if (title !== undefined) updateData.title = title;
    if (description !== undefined) updateData.description = description;
    if (company !== undefined) updateData.company = company;
    if (location !== undefined) updateData.location = location;
    if (salary !== undefined) updateData.salary = salary;
    if (requirements !== undefined) updateData.requirements = requirements;
    if (skills !== undefined) updateData.skills = skills;

    const { data, error } = await supabase
      .from('jobs')
      .update(updateData)
      .eq('id', id)
      .select()
      .single();

    if (error) throw error;

    if (!data) {
      return res.status(404).json({ error: 'Job not found' });
    }

    res.json({ 
      message: 'Job updated successfully',
      job: data 
    });
  } catch (error: any) {
    console.error('Error updating job:', error);
    res.status(500).json({ error: 'Failed to update job', message: error.message });
  }
});

// DELETE /api/jobs/:id - Delete job posting (admin only)
router.delete('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const { error } = await supabase
      .from('jobs')
      .delete()
      .eq('id', id);

    if (error) throw error;

    res.json({ message: 'Job deleted successfully' });
  } catch (error: any) {
    console.error('Error deleting job:', error);
    res.status(500).json({ error: 'Failed to delete job', message: error.message });
  }
});

export default router;
