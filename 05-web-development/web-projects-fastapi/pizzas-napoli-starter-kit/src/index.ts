import { Hono } from "hono";
import { pizzasRouter } from "./routes/pizzasRouter";
import { authRouter } from "./routes/authRouter";
import { ordersRouter } from "./routes/ordersRouter";

const app = new Hono();

app.get("/", (c) => {
  return c.json({
    message: "Welcome to Pizzas API",
    success: true
  });
});

app.get("/health", (c) => {
  return c.json({
    message: "Pizzas API is healthy",
    success: true
  });
});

//3 façon de gérer les routes

//1 - associer un ensemble de routes préfixées par /pizzas à un routeur
app.route("/pizzas", pizzasRouter);
app.route("/auth", authRouter);
app.route("/orders", ordersRouter);

//2 - associer un handler à une route
//app.get("/pizzas", (c) => GetPizzas(c));

//3 - gérer directement la route
// app.get("/pizzas/:id", (c) => {
//   const { id } = c.req.param();

//   const existingPizza = pizzas.filter((p) => p.id === Number(id));

//   if (existingPizza.length > 0) {
//     return c.json({
//       data: existingPizza,
//       message: "Pizza found",
//       success: true,
//       count: pizzas.length
//     });
//   } else {
//     return c.json({ status: false, message: "Pizza does not exist" }, 404);
//   }
// });

export default app;
