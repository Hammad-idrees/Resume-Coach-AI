import { Request, Response, NextFunction } from 'express';
import { supabase } from '../config/supabase';

export interface AuthenticatedRequest extends Request {
  user?: {
    id: string;
    email?: string;
  };
}

/**
 * Middleware to verify Supabase JWT token and attach user to request
 */
export async function authMiddleware(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    // Extract token from Authorization header
    const authHeader = req.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({ error: 'No authorization token provided' });
      return;
    }

    const token = authHeader.split('Bearer ')[1];

    // Verify token with Supabase
    const { data: { user }, error } = await supabase.auth.getUser(token);

    if (error || !user) {
      console.error('Auth error:', error);
      res.status(401).json({ error: 'Invalid or expired token' });
      return;
    }

    // Attach user to request object
    req.user = {
      id: user.id,
      email: user.email
    };

    next();
  } catch (error: any) {
    console.error('Auth middleware error:', error);
    res.status(500).json({ error: 'Authentication failed', message: error.message });
  }
}

/**
 * Optional middleware - allows both authenticated and anonymous access
 * If token is present, attaches user; otherwise continues without user
 */
export async function optionalAuthMiddleware(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> {
  try {
    const authHeader = req.headers.authorization;
    
    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.split('Bearer ')[1];
      const { data: { user } } = await supabase.auth.getUser(token);
      
      if (user) {
        req.user = {
          id: user.id,
          email: user.email
        };
      }
    }

    next();
  } catch (error) {
    // Continue without user on error
    next();
  }
}

/**
 * Middleware to extract user ID from x-user-id header (legacy support)
 * Use authMiddleware for proper JWT-based authentication
 */
export function legacyUserIdMiddleware(
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): void {
  const userId = req.headers['x-user-id'] as string;
  
  if (!userId) {
    res.status(401).json({ error: 'User ID required in x-user-id header' });
    return;
  }

  req.user = { id: userId };
  next();
}
