import { Router, Request, Response } from 'express';
import { supabase } from '../config/supabase';

const router = Router();

interface SignUpRequest {
  email: string;
  password: string;
  name?: string;
}

interface SignInRequest {
  email: string;
  password: string;
}

// POST /api/auth/signup - Register new user
router.post('/signup', async (req: Request, res: Response) => {
  try {
    const { email, password, name }: SignUpRequest = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    if (password.length < 6) {
      return res.status(400).json({ error: 'Password must be at least 6 characters' });
    }

    // Sign up with Supabase Auth
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          name: name || email.split('@')[0]
        }
      }
    });

    if (error) {
      console.error('Signup error:', error);
      return res.status(400).json({ error: error.message });
    }

    // Check if email confirmation is required
    if (data.user && !data.session) {
      return res.status(200).json({
        message: 'Registration successful! Please check your email to confirm your account.',
        user: {
          id: data.user.id,
          email: data.user.email
        },
        requiresEmailConfirmation: true
      });
    }

    res.status(201).json({
      message: 'Registration successful!',
      user: {
        id: data.user?.id,
        email: data.user?.email,
        name: data.user?.user_metadata?.name
      },
      session: {
        access_token: data.session?.access_token,
        refresh_token: data.session?.refresh_token,
        expires_at: data.session?.expires_at
      }
    });
  } catch (error: any) {
    console.error('Signup error:', error);
    res.status(500).json({ error: 'Registration failed', message: error.message });
  }
});

// POST /api/auth/signin - Login user
router.post('/signin', async (req: Request, res: Response) => {
  try {
    const { email, password }: SignInRequest = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    // Sign in with Supabase Auth
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    });

    if (error) {
      console.error('Sign in error:', error);
      return res.status(401).json({ error: 'Invalid email or password' });
    }

    res.json({
      message: 'Login successful!',
      user: {
        id: data.user.id,
        email: data.user.email,
        name: data.user.user_metadata?.name
      },
      session: {
        access_token: data.session.access_token,
        refresh_token: data.session.refresh_token,
        expires_at: data.session.expires_at
      }
    });
  } catch (error: any) {
    console.error('Sign in error:', error);
    res.status(500).json({ error: 'Login failed', message: error.message });
  }
});

// POST /api/auth/signout - Logout user
router.post('/signout', async (req: Request, res: Response) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.split('Bearer ')[1];
      
      if (token) {
        // Sign out from Supabase
        const { error } = await supabase.auth.admin.signOut(token);
        
        if (error) {
          console.error('Sign out error:', error);
        }
      }
    }

    res.json({ message: 'Logout successful' });
  } catch (error: any) {
    console.error('Sign out error:', error);
    res.status(500).json({ error: 'Logout failed', message: error.message });
  }
});

// GET /api/auth/me - Get current user
router.get('/me', async (req: Request, res: Response) => {
  try {
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No authorization token provided' });
    }

    const token = authHeader.split('Bearer ')[1];

    const { data: { user }, error } = await supabase.auth.getUser(token);

    if (error || !user) {
      return res.status(401).json({ error: 'Invalid or expired token' });
    }

    res.json({
      user: {
        id: user.id,
        email: user.email,
        name: user.user_metadata?.name,
        created_at: user.created_at
      }
    });
  } catch (error: any) {
    console.error('Get user error:', error);
    res.status(500).json({ error: 'Failed to get user', message: error.message });
  }
});

// POST /api/auth/refresh - Refresh access token
router.post('/refresh', async (req: Request, res: Response) => {
  try {
    const { refresh_token } = req.body;

    if (!refresh_token) {
      return res.status(400).json({ error: 'Refresh token required' });
    }

    const { data, error } = await supabase.auth.refreshSession({
      refresh_token
    });

    if (error) {
      console.error('Token refresh error:', error);
      return res.status(401).json({ error: 'Invalid refresh token' });
    }

    res.json({
      session: {
        access_token: data.session?.access_token,
        refresh_token: data.session?.refresh_token,
        expires_at: data.session?.expires_at
      }
    });
  } catch (error: any) {
    console.error('Token refresh error:', error);
    res.status(500).json({ error: 'Token refresh failed', message: error.message });
  }
});

// POST /api/auth/reset-password - Request password reset
router.post('/reset-password', async (req: Request, res: Response) => {
  try {
    const { email } = req.body;

    if (!email) {
      return res.status(400).json({ error: 'Email is required' });
    }

    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${process.env.FRONTEND_URL}/reset-password`
    });

    if (error) {
      console.error('Password reset error:', error);
      return res.status(400).json({ error: error.message });
    }

    res.json({ message: 'Password reset email sent. Please check your inbox.' });
  } catch (error: any) {
    console.error('Password reset error:', error);
    res.status(500).json({ error: 'Password reset failed', message: error.message });
  }
});

// POST /api/auth/update-password - Update password
router.post('/update-password', async (req: Request, res: Response) => {
  try {
    const authHeader = req.headers.authorization;
    const { password } = req.body;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No authorization token provided' });
    }

    if (!password || password.length < 6) {
      return res.status(400).json({ error: 'Password must be at least 6 characters' });
    }

    const token = authHeader.split('Bearer ')[1];

    // Verify user first
    const { data: { user }, error: userError } = await supabase.auth.getUser(token);

    if (userError || !user) {
      return res.status(401).json({ error: 'Invalid or expired token' });
    }

    // Update password
    const { error } = await supabase.auth.updateUser({ password });

    if (error) {
      console.error('Password update error:', error);
      return res.status(400).json({ error: error.message });
    }

    res.json({ message: 'Password updated successfully' });
  } catch (error: any) {
    console.error('Password update error:', error);
    res.status(500).json({ error: 'Password update failed', message: error.message });
  }
});

export default router;
