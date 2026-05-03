import { Router } from 'express';
import { register, login } from '../services/authService';
import { AppDataSource } from '../db';
import { DoctorPatient } from '../entity/DoctorPatient';

const router = Router();

router.post('/register', async (req, res) => {
  const { role, email, password, profile, attachToDoctorId } = req.body;
  if (!role || !email || !password) return res.status(400).json({ message: 'role, email, password required' });
  try {
    const token = await register(role, email, password, profile);
    // optionnel : rattacher un patient à un médecin
    if (role === 'PATIENT' && attachToDoctorId) {
      const patientUser = (require('jsonwebtoken').decode(token.accessToken) as any);
      const repo = AppDataSource.getRepository(DoctorPatient);
      await repo.save(repo.create({ doctorId: parseInt(attachToDoctorId,10), patientId: patientUser.id }));
    }
    res.json(token);
  } catch (e:any) {
    res.status(400).json({ message: e.message });
  }
});

router.post('/login', async (req,res) => {
  const { email, password } = req.body;
  if (!email || !password) return res.status(400).json({ message: 'email, password required' });
  try {
    const token = await login(email, password);
    res.json(token);
  } catch (e:any) {
    res.status(400).json({ message: e.message });
  }
});

export default router;
