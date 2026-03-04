import React, { useState } from "react";
import { ChevronDownIcon, ChevronRightIcon, Bars3Icon } from "@heroicons/react/24/solid";
import TestsTable from "./Table/TestsTable";

export default function BoardSection({ name, tests, onRun }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700 shadow-md hover:shadow-lg transition">
      
      {/* HEADER */}
      <div
        className="flex items-center justify-between px-4 py-3 cursor-pointer 
                   hover:bg-gray-700 rounded-t-xl"
        onClick={() => setOpen(!open)}
      >
        <div className="flex items-center gap-2">
          {open ? (
            <ChevronDownIcon className="w-5 h-5 text-gray-300" />
          ) : (
            <ChevronRightIcon className="w-5 h-5 text-gray-300" />
          )}
          
          <h3 className="text-lg font-semibold text-gray-100">{name}</h3>
          <span className="text-gray-400 text-sm">({tests.length} tests)</span>
        </div>

        <Bars3Icon className="w-5 h-5 text-gray-300" />
      </div>

      {/* CONTENT */}
      {open && (
        <div className="p-4 bg-gray-900 border-t border-gray-700 rounded-b-xl">
          <TestsTable boards={tests} onRun={onRun} />
        </div>
      )}
    </div>
  );
}
