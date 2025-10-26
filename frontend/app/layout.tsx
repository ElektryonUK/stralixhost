import "./globals.css";
import { AuthProvider } from "../components/auth/AuthProvider";
import { HeaderNav } from "../components/layout/HeaderNav";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <HeaderNav />
          <main>{children}</main>
        </AuthProvider>
      </body>
    </html>
  );
}
