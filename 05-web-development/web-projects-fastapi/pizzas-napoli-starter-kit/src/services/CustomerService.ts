import { Customer } from "../types";

//fake customers db table
const customers: Array<Customer> = [
  { id: 1, email: "fred@gmail.com", password: "azzreerizl" }
];

export class CustomerService {
  findAll(): Array<Customer> {
    return customers;
  }

  findByEmail(email: string): Customer | undefined {
    return customers.find((cs) => cs.email === email);
  }

  findById(id: number): Customer | undefined {
    return customers.find((cs) => cs.id === id);
  }
}
