import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '../config';

export interface AuthPayload { id: number; role: 'DOCTOR'|'PATIENT'; }

declare global {
  namespace Express {
    interface Request { user?: AuthPayload }
  }
}

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const hdr = req.headers['authorization'];
  if (!hdr) return res.status(401).json({ message: 'Missing Authorization header' });
  const token = hdr.replace('Bearer ', '');
  try {
    const payload = jwt.verify(token, config.jwtSecret) as AuthPayload;
    req.user = payload;
    next();
  } catch (e) {
    return res.status(401).json({ message: 'Invalid token' });
  }
}

export function requireRole(role: 'DOCTOR'|'PATIENT') {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) return res.status(401).json({ message: 'Unauthenticated' });
    if (req.user.role !== role) return res.status(403).json({ message: 'Forbidden' });
    next();
  }
}
