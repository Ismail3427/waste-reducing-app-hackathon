import { betterAuth } from "better-auth";
import { prismaAdapter } from "better-auth/adapters/prisma";
import prisma from "./prisma";
import { expo } from "@better-auth/expo";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: prismaAdapter(prisma, { provider: "postgresql" }),
  baseURL: "http://localhost:3000/",
  plugins: [
    expo(),
    jwt({
      jwt: {
        expirationTime: "30m",
        definePayload: ({ user }: { user: any }) => ({
          email: user.email,
          name: user.name,
          userId: user.sub,
        }),
      },
    }),
  ],
  emailAndPassword: { enabled: true },
});
