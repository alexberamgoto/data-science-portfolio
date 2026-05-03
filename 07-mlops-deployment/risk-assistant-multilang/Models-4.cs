// Models.cs
public class RiskRequest
{
    public string client_id { get; set; }
    public double amount { get; set; }
    public double income { get; set; }
    public int tenure_months { get; set; }
}

public class RiskResponse
{
    public string client_id { get; set; }
    public double risk_score { get; set; }
    public string risk_level { get; set; }
}

public class AnomalyRequest
{
    public string client_id { get; set; }
    public double amount { get; set; }
    public double balance { get; set; }
    public double tx_per_day { get; set; }
}

public class AnomalyResponse
{
    public string client_id { get; set; }
    public double anomaly_score { get; set; }
    public bool is_anomaly { get; set; }
}

public class RecoRequest
{
    public string client_id { get; set; }
    public double income { get; set; }
    public double risk_score { get; set; }
}

public class RecoResponse
{
    public string client_id { get; set; }
    public List<string> recommended_products { get; set; }
}
