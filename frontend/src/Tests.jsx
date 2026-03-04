import React, { useEffect, useState } from "react";
import TestsTable from "./components/Table/TestsTable";
import api from "./Services/api";

export default function Tests() {
  const [tests, setTests] = useState({}); 

  useEffect(() => {
    api.get("/testsuites").then(res => {
      setTests(res.data);   // ✔️ on garde la structure des boards
    });
  }, []);

  const runTest = (test) => {
    api.post("/run_test", test);
  };

  return (
    <div className="p-6">
      <h1 className="text-5xl font-bold">Configured Tests</h1>

      <TestsTable boards={tests} onRun={runTest} />
    </div>
  );
}