import { AppDataSource } from './db';
import { config } from './config';
import app from './app';

AppDataSource.initialize().then(() => {
  app.listen(config.port, () => console.log(`API REST listening on :${config.port}`));
}).catch((err) => {
  console.error('DB init failed', err);
  process.exit(1);
});
