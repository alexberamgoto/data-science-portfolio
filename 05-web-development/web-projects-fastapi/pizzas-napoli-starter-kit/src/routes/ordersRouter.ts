import { Hono } from "hono";
import { PizzaSelection, Pizza } from "../types";
import { PizzaService } from "../services/PizzaService";

const pizzaService = new PizzaService();

const pizzas = pizzaService.findAll();

export const ordersRouter = new Hono();

ordersRouter.post("/", async (c) => {
  //1 - récupère les données utiles dans le body
  const body: Array<PizzaSelection> = await c.req.json();

  let amount: number = 0;
  let pizzaQuantity: number = 0;

  //2 - vérifier si les pizzas existent
  const allPizzasExist: boolean = body.every((p) =>
    pizzas.find((pz) => pz.id === p.pizzaId)
  );

  if (!allPizzasExist) {
    return c.json(
      { success: false, message: "Some pizza does not exist" },
      409
    );
  }

  //3 - calcule le total de la commande

  body.forEach((pizzaSelection) => {
    const existingPizza: Pizza | undefined = pizzas.find(
      (pz) => pz.id === pizzaSelection.pizzaId
    );

    if (existingPizza) {
      amount += existingPizza.price * pizzaSelection.quantity;
      pizzaQuantity += pizzaSelection.quantity;
    } else {
      //déclencher une erreur car une pizza sélectionnée n'existe pas
    }
  });

  //4 - réponse
  return c.json(
    {
      success: true,
      message: "Order created",
      amount: amount,
      pizzasRecipesQuantity: body.length,
      pizzasQuantity: pizzaQuantity
    },
    201
  );
});
