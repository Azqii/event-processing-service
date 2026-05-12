import http from "k6/http";
import { check } from "k6";

export const options = {
  vus: 1,
  iterations: Number(__ENV.ITERATIONS || 10),
  summaryTrendStats: ["avg", "p(95)"],
};

const token = __ENV.TOKEN;
const endpoint = __ENV.ENDPOINT;

export default function () {
  const payload = JSON.stringify({
    event_type: "user.login",
    occurred_at: "2026-05-12T10:00:00Z",
    payload: {
      user_id: `benchmark-user-${__ITER}`,
    },
  });

  const params = {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  };

  const response = http.post(endpoint, payload, params);

  check(response, {
    "status is successful": (r) => r.status === 200 || r.status === 202,
  });
}

export function handleSummary(data) {
  const duration = data.metrics.http_req_duration.values;
  const failed = data.metrics.http_req_failed.values;
  const checks = data.metrics.checks.values;
  const iterations = data.metrics.iterations.values.count;
  const totalTimeMs = data.state.testRunDurationMs;

  return {
    stdout:
      `endpoint: ${endpoint}\n` +
      `iterations: ${iterations}\n` +
      `total_time_ms: ${totalTimeMs.toFixed(2)}\n` +
      `avg_ms: ${duration.avg.toFixed(2)}\n` +
      `p95_ms: ${duration["p(95)"].toFixed(2)}\n` +
      `failed_rate: ${(failed.rate * 100).toFixed(2)}%\n` +
      `checks_rate: ${(checks.rate * 100).toFixed(2)}%\n`,
  };
}