import { Entity, PrimaryGeneratedColumn, Column } from 'typeorm';

@Entity()
export class Patient {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  userId!: number;

  @Column({ default: '' })
  firstName!: string;

  @Column({ default: '' })
  lastName!: string;

  @Column({ type: 'date', nullable: true })
  dateOfBirth!: string | null;
}
