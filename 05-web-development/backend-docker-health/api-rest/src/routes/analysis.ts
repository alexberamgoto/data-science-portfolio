import { Router } from 'express';
import { authMiddleware } from '../middleware/auth';
import { analyzeHealthData } from '../services/mlClient';
import { AppDataSource } from '../db';
import { AnalysisResult } from '../entity/AnalysisResult';

const router = Router();
router.use(authMiddleware);

router.post('/request', async (req,res) => {
  // Si patient: analyse ses dernières données. Si médecin: peut passer { patientId }
  const payload = req.user!;
  const patientId = payload.role === 'PATIENT' ? payload.id : (req.body.patientId as number);
  if (!patientId) return res.status(400).json({ message: 'patientId required for doctors' });

  const snapshot = { patientId, ...req.body.metrics };
  try {
    const result = await analyzeHealthData(snapshot);
    const repo = AppDataSource.getRepository(AnalysisResult);
    const rec = repo.create({ patientId, inputSnapshot: snapshot, score: result.score, riskLevel: result.riskLevel, explanation: result.explanation });
    await repo.save(rec);
    res.json(rec);
  } catch (e:any) {
    res.status(502).json({ message: e.message });
  }
});

export default router;
