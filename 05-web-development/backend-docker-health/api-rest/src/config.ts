import dotenv from 'dotenv';
dotenv.config();
export const config = {
  port: parseInt(process.env.PORT || '3000', 10),
  jwtSecret: process.env.JWT_SECRET || 'dev_secret',
  db: {
    host: process.env.POSTGRES_HOST || 'db-rest',
    port: parseInt(process.env.POSTGRES_PORT || '5432', 10),
    database: process.env.POSTGRES_DB || 'healthdb',
    username: process.env.POSTGRES_USER || 'health',
    password: process.env.POSTGRES_PASSWORD || 'healthpwd',
  },
  ml: {
    baseUrl: process.env.ML_BASE_URL || 'http://api-ml:8000'
  }
};
