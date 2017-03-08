-- frankly this is annoying. there's no option in wrk to suppress the default
-- report output. I just want JSON here. However, I'm outputting to a single
-- line so it's easy to grep the json only, just do
--
--      wrk ... | grep json_output | jq ...
--
-- https://github.com/wg/wrk/blob/50305ed1d89408c26067a970dcd5d9dbea19de9d/SCRIPTING

done = function(summary, latency, requests)
    io.write("------------------------------ json:\n")
    io.write(string.format(
        "{\"json_output\":{\"requests_sec\":%.2f,\"avg_latency_ms\":%.2f}}",
        summary.requests/(summary.duration/1000000),
        (latency.mean/1000)
        ))
end
