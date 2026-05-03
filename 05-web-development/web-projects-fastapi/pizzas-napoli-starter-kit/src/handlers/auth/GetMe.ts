import { Context } from "hono";
import { CustomerService } from "../../services/CustomerService";
import { Customer } from "../../types";

export const GetMe = async (c: Context) => {
  const jwtPayload = c.get("jwtPayload");

  const customerService = new CustomerService();

  const customer: Customer | undefined = customerService.findById(
    jwtPayload.customerId
  );

  if (!customer) {
    return c.json({ success: false, error: "Customer does not exist" }, 404);
  }

  const { password, ...customerWithoutPassword } = customer;

  return c.json(customerWithoutPassword, 200);
};
