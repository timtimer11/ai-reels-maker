import "./globals.css";
import { Inter } from "next/font/google";
import {
  Menubar,
  MenubarMenu,
  MenubarTrigger,
} from "@/components/ui/menubar";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "Brain Rot App",
  description: "Generate your brain rot video",
};

function MenubarDemo() {
  return (
    <Menubar className="flex justify-center">
      <div className="flex space-x-4">
        <MenubarMenu>
          <MenubarTrigger>Home</MenubarTrigger>
        </MenubarMenu>
        <MenubarMenu>
          <MenubarTrigger>Features</MenubarTrigger>
        </MenubarMenu>
        <MenubarMenu>
          <MenubarTrigger>Limits</MenubarTrigger>
        </MenubarMenu>
        <MenubarMenu>
          <MenubarTrigger>Contact</MenubarTrigger>
        </MenubarMenu>
        <MenubarMenu>
          <MenubarTrigger>Launch App</MenubarTrigger>
        </MenubarMenu>
      </div>
    </Menubar>
  )
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
          <MenubarDemo />
          {children}
      </body>
    </html>
  );
}
