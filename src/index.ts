import { createDbWorker } from "sql.js-httpvfs";
import {QuixSql} from "./quix"

const workerUrl = new URL(
  "sql.js-httpvfs/dist/sqlite.worker.js",
  import.meta.url
);
const wasmUrl = new URL("sql.js-httpvfs/dist/sql-wasm.wasm", import.meta.url);

async function load() {
  const worker = await createDbWorker(
    [
      {
        from: "inline",
        config: {
          serverMode: "full",
          url: "/dq.db",
          requestChunkSize: 1024,
        },
      },
    ],
    workerUrl.toString(),
    wasmUrl.toString()
  );

  const dq = new QuixSql(worker);
  
  const result = await dq.generate_fragment()
  document.body.textContent = JSON.stringify(result);
}

load();
