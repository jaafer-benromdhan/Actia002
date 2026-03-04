import React, { useEffect, useMemo, useState } from "react";
import api from "./Services/api";
import Sidebar from "./components/Sidebar/Sidebar";
import BoardSection from "./components/BoardSection";
import { Bars3Icon } from "@heroicons/react/24/solid";

export default function App() {
  const [boards, setBoards] = useState({});           // { C031: [...], F411: [...], ... }
  const [selectedBoard, setSelectedBoard] = useState("ALL");
  const [search, setSearch] = useState("");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    api.get("/testsuites").then(res => {
      setBoards(res.data || {});
    });
  }, []);

  const runTest = (test) => {
    api.post("/run_test", test);
  };

  const runAllInBoard = () => {
    const list =
      selectedBoard === "ALL"
        ? Object.values(boards).flat()
        : boards[selectedBoard] || [];
    if (!list.length) return;
    // Exécution séquentielle simple (tu peux paralléliser si besoin)
    list.forEach(t => api.post("/run_test", t));
  };

  const filteredBoardKeys = useMemo(() => {
    const keys = Object.keys(boards);
    if (!search.trim()) return ["ALL", ...keys];
    const q = search.toLowerCase();
    const filtered = keys.filter(k => k.toLowerCase().includes(q));
    return ["ALL", ...filtered];
  }, [boards, search]);

  const visibleBoards = useMemo(() => {
    if (selectedBoard === "ALL") {
      return filteredBoardKeys.filter(k => k !== "ALL");
    }
    return filteredBoardKeys.includes(selectedBoard) ? [selectedBoard] : [];
  }, [filteredBoardKeys, selectedBoard]);

  return (
    <div className="min-h-screen bg-gray-100 flex">
      {/* SIDEBAR (desktop & mobile via overlay) */}
      <Sidebar
        boards={boards}
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        selectedBoard={selectedBoard}
        onSelectBoard={(key) => {
          setSelectedBoard(key);
          setSidebarOpen(false);
        }}
        search={search}
        onSearch={setSearch}
      />

      {/* MAIN CONTENT */}
      <div className="flex-1 min-w-0">
        {/* Topbar */}
        <div className="sticky top-0 z-20 bg-white border-b border-gray-200 px-4 sm:px-6 py-3 flex items-center gap-3">
          {/* Hamburger for mobile */}
          <button
            className="md:hidden inline-flex items-center justify-center rounded-md p-2 hover:bg-gray-100"
            onClick={() => setSidebarOpen(true)}
            aria-label="Open sidebar"
          >
            <Bars3Icon className="w-6 h-6 text-gray-700" />
          </button>

          <div className="flex-1 flex items-center justify-between">
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight">
              Configured Tests
            </h1>

            <button
              onClick={runAllInBoard}
              className="hidden sm:inline-flex bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium px-4 py-2 rounded-lg shadow"
            >
              Run All {selectedBoard !== "ALL" ? `(${selectedBoard})` : ""}
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-4 sm:p-6 space-y-6">
          {visibleBoards.length === 0 && (
            <div className="text-gray-500">Aucun board à afficher.</div>
          )}

          {visibleBoards.map((boardName) => (
            <BoardSection
              key={boardName}
              name={boardName}
              tests={boards[boardName] || []}
              onRun={runTest}
            />
          ))}

          {/* Bouton Run All aussi en bas pour mobile */}
          <div className="sm:hidden sticky bottom-4 flex justify-end pr-2">
            <button
              onClick={runAllInBoard}
              className="bg-emerald-600 hover:bg-emerald-700 text-white text-sm font-medium px-4 py-2 rounded-full shadow"
            >
              Run All {selectedBoard !== "ALL" ? `(${selectedBoard})` : ""}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}