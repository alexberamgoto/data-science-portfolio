import { Router } from 'express';
import { authMiddleware, requireRole } from '../middleware/auth';
import { AppDataSource } from '../db';
import { HealthData } from '../entity/HealthData';

const router = Router();
router.use(authMiddleware);

router.post('/data', requireRole('PATIENT'), async (req,res) => {
  const repo = AppDataSource.getRepository(HealthData);
  const data = repo.create({ patientId: req.user!.id, ...req.body });
  await repo.save(data);
  res.json({ id: data.id });
});

router.get('/data/history', requireRole('PATIENT'), async (req,res) => {
  const repo = AppDataSource.getRepository(HealthData);
  const rows = await repo.find({ where: { patientId: req.user!.id }, order: { createdAt: 'DESC' } as any });
  res.json(rows);
});

export default router;
