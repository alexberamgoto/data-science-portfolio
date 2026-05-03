import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity()
export class DoctorPatient {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  doctorId!: number;

  @Column()
  patientId!: number;
}
