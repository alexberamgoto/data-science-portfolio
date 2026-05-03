import { Hono } from "hono";
import { GetPizzas } from "../handlers/pizzas/GetPizzas";
import { PizzaService } from "../services/PizzaService";

const pizzaService = new PizzaService();

const pizzas = pizzaService.findAll();

export const pizzasRouter = new Hono();

pizzasRouter.get("/", (c) => GetPizzas(c));

pizzasRouter.get("/", (c) => GetPizzas(c));

pizzasRouter.get("/:id", (c) => {
  const { id } = c.req.param();

  const existingPizza = pizzas.filter((p) => p.id === Number(id));

  if (existingPizza.length > 0) {
    return c.json({
      data: existingPizza,
      message: "Pizza found",
      success: true,
      count: pizzas.length
    });
  } else {
    return c.json({ status: false, message: "Pizza does not exist" }, 404);
  }
});
