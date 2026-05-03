import { Router } from 'express';
import { authMiddleware, requireRole } from '../middleware/auth';
import { AppDataSource } from '../db';
import { DoctorPatient } from '../entity/DoctorPatient';
import { HealthData } from '../entity/HealthData';

const router = Router();
router.use(authMiddleware, requireRole('DOCTOR'));

router.get('/patients', async (req,res) => {
  const repo = AppDataSource.getRepository(DoctorPatient);
  const links = await repo.find();
  const patients = links.filter(l => l.doctorId === req.user!.id).map(l => l.patientId);
  res.json({ patientIds: patients });
});

router.get('/patients/:id/data', async (req,res) => {
  const patientId = parseInt(req.params.id,10);
  const repoLink = AppDataSource.getRepository(DoctorPatient);
  const link = await repoLink.findOne({ where: { doctorId: req.user!.id, patientId } });
  if (!link) return res.status(403).json({ message: 'Not linked to this patient' });
  const repo = AppDataSource.getRepository(HealthData);
  const rows = await repo.find({ where: { patientId }, order: { createdAt: 'DESC' } as any });
  res.json(rows);
});

export default router;
