import { Context, Next } from "hono";
import { verify } from "jsonwebtoken";

export async function checkBearerAuth(c: Context, next: Next) {
  //récupère le header HTTP authorization
  const authHeader = c.req.header("Authorization");

  //vérifie que le Header Authorization contient une valeur de type Bearer avec un token JWT
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    //si ce n'est pas le cas, retourne une erreur
    return c.json({ message: "Bearer authentication required" }, 401);
  }

  //récupère le token JWT dans le header HTTP authorization Bearer
  const token = authHeader.slice(7);

  //vérifie que le token JWT est valide
  const payload = verify(token, Bun.env.JWT_SECRET ?? "");

  //si ce n'est pas le cas, retourne une erreur
  if (!payload) {
    return c.json({ message: "Invalid or expired token" }, 401);
  }

  c.set("jwtPayload", payload); //transmet les données extraites du token JWT au prochain handler

  await next(); //passe la main au prochain handler
}
