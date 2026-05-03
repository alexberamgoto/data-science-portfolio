import { Context } from "hono";
import { PizzaService } from "../../services/PizzaService";
import { Pizza } from "../../types";

export const GetPizzas = (c: Context) => {
  const service = new PizzaService();
  const pizzas: Array<Pizza> = service.findAll();

  return c.json({
    data: pizzas,
    message: "Pizzas list",
    success: true,
    count: pizzas.length
  });
};
