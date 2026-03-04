export default function TestsTable({ boards, onRun }) {
  if (!boards) return null;

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm text-gray-200">
        <thead className="bg-gray-700 text-gray-300">
          <tr>
            <th className="p-3 text-left">Test</th>
            <th className="p-3 text-left">File</th>
            <th className="p-3 text-left">Address</th>
            <th className="p-3 text-left">MCU</th>
            <th className="p-3 text-left">Interface</th>
            <th className="p-3 text-left">Reset</th>
            <th className="p-3 text-left">Action</th>
          </tr>
        </thead>

        <tbody>
          {boards.map((t, i) => (
            <tr
              key={i}
              className="border-b border-gray-700 bg-gray-800 hover:bg-gray-700"
            >
              <td className="p-3">{t.name}</td>
              <td className="p-3">{t.file}</td>
              <td className="p-3">{t.address}</td>
              <td className="p-3">{t.mcu}</td>
              <td className="p-3">{t.interface}</td>
              <td className="p-3">{t.reset ? "Yes" : "No"}</td>
              <td className="p-3">
                <button
                  onClick={() => onRun(t)}
                  className="px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md"
                >
                  Run
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
