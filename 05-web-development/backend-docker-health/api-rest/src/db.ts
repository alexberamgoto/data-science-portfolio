import 'reflect-metadata';
import { DataSource } from 'typeorm';
import { config } from './config';
import { User } from './entity/User';
import { Doctor } from './entity/Doctor';
import { Patient } from './entity/Patient';
import { DoctorPatient } from './entity/DoctorPatient';
import { HealthData } from './entity/HealthData';
import { AnalysisResult } from './entity/AnalysisResult';

export const AppDataSource = new DataSource({
  type: 'postgres',
  host: config.db.host,
  port: config.db.port,
  username: config.db.username,
  password: config.db.password,
  database: config.db.database,
  entities: [User, Doctor, Patient, DoctorPatient, HealthData, AnalysisResult],
  synchronize: true, // dev only
  logging: false,
});
