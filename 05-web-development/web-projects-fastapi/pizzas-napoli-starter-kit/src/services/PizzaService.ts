import { Pizza } from "../types";

//fake pizzas db table
const pizzas: Array<Pizza> = [
  {
    id: 1,
    name: "Margherita",
    ingredients: ["Tomate", "Mozzarella"],
    price: 7
  },
  {
    id: 2,
    name: "4 formaggi",
    ingredients: [
      "Crème",
      "Mozzarella",
      "Parmesan",
      "Gorgonzola",
      "Mascarpone"
    ],
    price: 12
  }
];

export class PizzaService {
  findById(id: number): Pizza | undefined {
    return pizzas.find((pz) => pz.id === id);
  }

  findAll(): Array<Pizza> {
    return pizzas;
  }
}
