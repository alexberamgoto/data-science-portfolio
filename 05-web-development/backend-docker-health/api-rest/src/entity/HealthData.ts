import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity()
export class HealthData {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  patientId!: number;

  @Column({ type: 'timestamptz', default: () => 'CURRENT_TIMESTAMP' })
  createdAt!: Date;

  @Column({ type: 'float', nullable: true })
  weight!: number | null;

  @Column({ type: 'int', nullable: true })
  systolic!: number | null;

  @Column({ type: 'int', nullable: true })
  diastolic!: number | null;

  @Column({ type: 'float', nullable: true })
  glucose!: number | null; // g/L

  @Column({ type: 'text', nullable: true })
  notes!: string | null;
}
