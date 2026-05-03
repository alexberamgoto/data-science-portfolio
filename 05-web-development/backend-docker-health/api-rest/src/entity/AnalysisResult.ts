import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity()
export class AnalysisResult {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  patientId!: number;

  @Column({ type: 'timestamptz', default: () => 'CURRENT_TIMESTAMP' })
  createdAt!: Date;

  @Column({ type: 'jsonb' })
  inputSnapshot!: any;

  @Column({ type: 'float' })
  score!: number;

  @Column({ type: 'varchar' })
  riskLevel!: string;

  @Column({ type: 'text', nullable: true })
  explanation!: string | null;
}
