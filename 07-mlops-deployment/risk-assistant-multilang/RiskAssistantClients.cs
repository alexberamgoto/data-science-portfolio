// RiskAssistantClient.cs
using System;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

public class RiskAssistantClient
{
    private readonly HttpClient _httpClient;

    public RiskAssistantClient(string baseUrl = "http://localhost:8000")
    {
        _httpClient = new HttpClient
        {
            BaseAddress = new Uri(baseUrl)
        };
    }

    public async Task<RiskResponse> GetRiskScoreAsync(RiskRequest req)
    {
        var response = await _httpClient.PostAsJsonAsync("/score_risque", req);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<RiskResponse>();
    }

    public async Task<AnomalyResponse> DetectAnomalyAsync(AnomalyRequest req)
    {
        var response = await _httpClient.PostAsJsonAsync("/detect_anomalie", req);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<AnomalyResponse>();
    }

    public async Task<RecoResponse> GetRecommendationsAsync(RecoRequest req)
    {
        var response = await _httpClient.PostAsJsonAsync("/reco_financiere", req);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<RecoResponse>();
    }
}
