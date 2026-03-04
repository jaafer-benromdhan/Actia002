import React from "react";
import {
  HomeIcon,
  WrenchScrewdriverIcon,
  Cog6ToothIcon,
  XMarkIcon,
} from "@heroicons/react/24/outline";
import { Squares2X2Icon } from "@heroicons/react/24/solid";

export default function Sidebar({ open, onClose }) {
  const NavItem = ({ Icon, label }) => (
    <button
      className="w-full flex items-center gap-3 px-4 py-2 rounded-lg
                 hover:bg-gray-800 transition dark:text-gray-200 text-gray-800"
    >
      <Icon className="w-5 h-5 text-gray-400 dark:text-gray-300" />
      <span>{label}</span>
    </button>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden md:flex flex-col w-64 bg-gray-900 dark:bg-gray-900 text-gray-100 border-r border-gray-700">
        <div className="px-4 py-5 flex items-center gap-2 border-b border-gray-700">
          <Squares2X2Icon className="w-6 h-6 text-indigo-400" />
          <h1 className="text-lg font-bold">Dashboard</h1>
        </div>

        <nav className="px-3 py-4 space-y-2">
          <NavItem Icon={HomeIcon} label="Home" />
          <NavItem Icon={WrenchScrewdriverIcon} label="Tests" />
          <NavItem Icon={Cog6ToothIcon} label="Settings" />
        </nav>
      </aside>

      {/* Mobile overlay */}
      <div
        className={[
          "fixed inset-0 bg-black/40 z-40 md:hidden",
          open ? "opacity-100" : "opacity-0 pointer-events-none",
        ].join(" ")}
        onClick={onClose}
      />

      {/* Mobile Sidebar */}
      <aside
        className={[
          "fixed z-50 inset-y-0 left-0 w-64 bg-gray-900 text-gray-100 border-r border-gray-700 md:hidden transition-transform",
          open ? "translate-x-0" : "-translate-x-full",
        ].join(" ")}
      >
        <div className="px-4 py-4 flex items-center justify-between border-b border-gray-700">
          <div className="flex items-center gap-2">
            <Squares2X2Icon className="w-6 h-6 text-indigo-400" />
            <h1 className="text-lg font-bold">Dashboard</h1>
          </div>

          <button className="p-2 hover:bg-gray-800 rounded-lg" onClick={onClose}>
            <XMarkIcon className="w-6 h-6 text-gray-200" />
          </button>
        </div>

        <nav className="px-3 py-4 space-y-2">
          <NavItem Icon={HomeIcon} label="Home" />
          <NavItem Icon={WrenchScrewdriverIcon} label="Tests" />
          <NavItem Icon={Cog6ToothIcon} label="Settings" />
        </nav>
      </aside>
    </>
  );
}
