export type Pizza = {
  id: number;
  name: string;
  ingredients: Array<string>;
  price: number;
};

export type Customer = {
  id: number;
  email: string;
  password: string;
};

export type CustomerCredentials = {
  email: string;
  password: string;
};

export type PizzaSelection = { pizzaId: number; quantity: number };
