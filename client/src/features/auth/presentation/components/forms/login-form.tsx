"use client";

import { useRef } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { cn } from "@/lib/utils";
import TextFormField from "@/features/shared/presentation/components/forms/text-form-field";
import { authClient } from "@/lib/auth-client";
import { appToast } from "@/features/shared/presentation/components/notifications/toast";
import { getAuthErrorMessage } from "@/lib/auth-errors";
import SubmitButton from "@/features/shared/presentation/components/custom-buttons/submit-button";

export function LoginForm({
  className,
  ...props
}: React.ComponentProps<"form">) {
  const router = useRouter();
  const formRef = useRef<HTMLFormElement>(null);

  const handleSubmit = async (formData: FormData) => {
    const email = formData.get("email") as string;
    const password = formData.get("password") as string;

    await authClient.signIn.email(
      {
        email,
        password,
        callbackURL: "/home",
        rememberMe: false,
      },
      {
        onSuccess: () => {
          formRef.current?.reset();
          appToast.success("¡Bienvenido de vuelta!");
          router.push("/home");
        },
        onError: (ctx) => {
          appToast.error(
            "Error al iniciar sesión",
            getAuthErrorMessage(ctx.error.code),
          );
        },
      },
    );
  };

  return (
    <form
      ref={formRef}
      action={handleSubmit}
      className={cn("space-y-6 w-full", className)}
      {...props}
    >
      <TextFormField
        id="email"
        name="email"
        label="Correo electrónico"
        placeholder="ejemplo@correo.com"
        type="email"
        autoComplete="email"
        required
      />

      <div className="space-y-1.5">
        <TextFormField
          id="password"
          name="password"
          label="Contraseña"
          placeholder="Tu contraseña"
          type="password"
          autoComplete="current-password"
          required
        />
        <div className="flex justify-end pt-0.5">
          <Link
            href="/auth/forgot-password"
            className="text-xs font-semibold text-[#6355DE] hover:underline"
          >
            ¿Olvidaste tu contraseña?
          </Link>
        </div>
      </div>

      <div className="pt-2">
        <SubmitButton
          text="Iniciar sesión"
          pendingText="Iniciando sesión..."
          className="w-full py-4 px-6 bg-[#6355DE] hover:bg-[#5244cc] active:scale-[0.99] text-white font-bold text-base rounded-full shadow-md shadow-[#6355DE]/20 transition-all duration-150 h-[52px]"
        />
      </div>
    </form>
  );
}
