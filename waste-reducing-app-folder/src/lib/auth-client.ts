import { createAuthClient } from "better-auth/react";
import { expoClient } from "@better-auth/expo/client";
import * as SecureStore from "expo-secure-store";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: "http://localhost:8081",
  plugins: [
    expoClient({
      scheme: "wastereducingappfolder",
      storagePrefix: "wastereducingapp",
      storage: SecureStore,
    }),
    jwtClient()
  ],
});
