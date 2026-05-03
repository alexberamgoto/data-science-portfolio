import { Hono } from "hono";
import { checkBearerAuth } from "../middlewares/checkBearerAuth";
import { sign } from "jsonwebtoken";
import { GetMe } from "../handlers/auth/GetMe";
import { CustomerCredentials, Customer } from "../types";
import { CustomerService } from "../services/CustomerService";

const customerService = new CustomerService();
const customers = customerService.findAll();

export const authRouter = new Hono();

authRouter.get("/me", checkBearerAuth, (c) => GetMe(c));

authRouter.post("/login", async (c) => {
  const credentials: CustomerCredentials = await c.req.json();

  const existingCustomer = customerService.findByEmail(credentials.email);

  if (!existingCustomer) {
    return c.json(
      {
        message: `User with email ${credentials.email} does not exist`,
        success: false
      },
      401
    );
  } else {
    const isValid = await Bun.password.verify(
      credentials.password,
      existingCustomer.password
    );

    if (isValid) {
      const access_token = sign(
        { customerId: existingCustomer.id },
        Bun.env.JWT_SECRET ?? "some-dummy-secret"
      );

      return c.json(
        {
          success: true,
          message: "Customer signed in",
          data: {
            access_token: access_token
          }
        },
        200
      );
    } else {
      return c.json(
        {
          message: `Wrong password`,
          success: false
        },
        401
      );
    }
  }
});

authRouter.post("/register", async (c) => {
  const valueInBody = await c.req.json();

  if ("id" in valueInBody) {
    return c.json({ message: "Value should not contain id" }, 400);
  }

  const body: Omit<Customer, "id"> = await c.req.json();

  //customers.push(body);//ici l'ajout n'est pas autorisé car l'attribut id est manquant

  //chiffre le mdp fourni en clair
  //https://bun.com/docs/guides/util/hash-a-password
  const hash = await Bun.password.hash(body.password);

  const customer: Customer = {
    ...body,
    id: customers.length + 1,
    password: hash //on enregistre la version chiffrée du mdp
  };

  const existingCustomer: boolean = customers.some(
    (cust) => cust.id === customer.id
  );

  if (existingCustomer) {
    return c.json({ message: `User with ${customer.id} already exists` }, 409);
  }

  customers.push(customer); //ici l'ajout est autorisé car il s'agit bien d'un objet de type Customer

  const { password, ...customerWithoutPassword } = customer; //on retire l'attribut password

  return c.json({
    success: true,
    message: "User created",
    data: customerWithoutPassword
  });
});
