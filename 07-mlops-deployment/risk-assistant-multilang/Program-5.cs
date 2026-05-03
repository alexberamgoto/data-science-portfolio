// Program.cs
using System;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        var client = new RiskAssistantClient("http://localhost:8000");

        var riskReq = new RiskRequest
        {
            client_id = "C123",
            amount = 2500,
            income = 3000,
            tenure_months = 24
        };

        var riskRes = await client.GetRiskScoreAsync(riskReq);
        Console.WriteLine($"Client {riskRes.client_id} – Score: {riskRes.risk_score:F3} – Niveau: {riskRes.risk_level}");

        var anomalyReq = new AnomalyRequest
        {
            client_id = "C123",
            amount = 2500,
            balance = 500,
            tx_per_day = 20
        };

        var anomalyRes = await client.DetectAnomalyAsync(anomalyReq);
        Console.WriteLine($"Anomaly: {anomalyRes.is_anomaly} – score: {anomalyRes.anomaly_score:F3}");

        var recoReq = new RecoRequest
        {
            client_id = "C123",
            income = 3000,
            risk_score = riskRes.risk_score
        };

        var recoRes = await client.GetRecommendationsAsync(recoReq);
        Console.WriteLine("Recommandations :");
        foreach (var p in recoRes.recommended_products)
        {
            Console.WriteLine($" - {p}");
        }
    }
}
