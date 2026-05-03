import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { AppDataSource } from '../db';
import { User } from '../entity/User';
import { Doctor } from '../entity/Doctor';
import { Patient } from '../entity/Patient';
import { DoctorPatient } from '../entity/DoctorPatient';
import { config } from '../config';

export async function register(role: 'DOCTOR'|'PATIENT', email: string, password: string, profile: any) {
  const userRepo = AppDataSource.getRepository(User);
  const existing = await userRepo.findOne({ where: { email } });
  if (existing) throw new Error('Email already registered');
  const passwordHash = await bcrypt.hash(password, 10);
  const user = userRepo.create({ email, passwordHash, role });
  await userRepo.save(user);
  if (role === 'DOCTOR') {
    const repo = AppDataSource.getRepository(Doctor);
    await repo.save(repo.create({ userId: user.id, firstName: profile?.firstName || '', lastName: profile?.lastName || '' }));
  } else {
    const repo = AppDataSource.getRepository(Patient);
    await repo.save(repo.create({ userId: user.id, firstName: profile?.firstName || '', lastName: profile?.lastName || '', dateOfBirth: profile?.dateOfBirth || null }));
  }
  const token = jwt.sign({ id: user.id, role: user.role }, config.jwtSecret, { expiresIn: '1h' });
  return { accessToken: token };
}

export async function login(email: string, password: string) {
  const userRepo = AppDataSource.getRepository(User);
  const user = await userRepo.findOne({ where: { email } });
  if (!user) throw new Error('Invalid credentials');
  const ok = await bcrypt.compare(password, user.passwordHash);
  if (!ok) throw new Error('Invalid credentials');
  const token = jwt.sign({ id: user.id, role: user.role }, config.jwtSecret, { expiresIn: '1h' });
  return { accessToken: token };
}
