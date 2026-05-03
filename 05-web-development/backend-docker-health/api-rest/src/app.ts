import express from 'express';
import cors from 'cors';
import bodyParser from 'body-parser';
import 'express-async-errors';

import authRoutes from './routes/auth';
import patientRoutes from './routes/patients';
import doctorRoutes from './routes/doctors';
import analysisRoutes from './routes/analysis';

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.use('/auth', authRoutes);
app.use('/patients', patientRoutes);
app.use('/doctors', doctorRoutes);
app.use('/analysis', analysisRoutes);

app.get('/health', (_,res) => res.json({ status: 'ok' }));

export default app;
