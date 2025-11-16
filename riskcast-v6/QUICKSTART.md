# RISKCAST v5.5 - Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```powershell
cd "c:\Users\ADMIN\Desktop\aav2\riskcast-v6"
pip install -r requirements.txt
```

### Step 2: Activate Virtual Environment (if using venv)
```powershell
.\venv\Scripts\Activate.ps1
```

### Step 3: Run the Application
```powershell
python run.py
```

The app will open at `http://localhost:8501`

---

## 📊 Using the Application

### Input Parameters (Sidebar)

1. **Giá trị (USD)** - Cargo value in dollars
   - Default: $39,000
   - Range: $1,000 to $10,000,000+

2. **Tuyến** - Shipping route
   - VN - EU (Vietnam to Europe)
   - VN - US (Vietnam to USA)
   - VN - Singapore
   - VN - China
   - Domestic

3. **Tháng** - Month for analysis
   - 1-12 (January-December)
   - Affects historical risk data

4. **Mục tiêu** - Priority profile
   - 💰 Tiết kiệm chi phí (Cost-focused)
   - ⚖️ Cân bằng (Balanced)
   - 🛡️ An toàn tối đa (Safety-focused)

5. **Model Configuration**
   - ☑️ Fuzzy AHP - Handle uncertainty in criteria weights
   - ☑️ ARIMA - Time series forecasting (optional)
   - ☑️ Monte Carlo - Risk simulation (optional)
   - ☑️ VaR/CVaR - Financial risk metrics (optional)

6. **MC Runs** - Number of simulations (500-5000)
7. **Fuzzy %** - Uncertainty level (0-50%)

---

## 🎯 Analyzing 15 Insurance Options

### Click "PHÂN TÍCH 15 PHƯƠNG ÁN" Button

The system analyzes:
- **5 Companies**: Chubb, PVI, BaoViet, BaoMinh, MIC
- **3 ICC Packages**:
  - **ICC A**: 100% coverage (1.5× premium)
  - **ICC B**: 75% coverage (1.0× premium)
  - **ICC C**: 50% coverage (0.65× premium)
- **Total**: 5 × 3 = **15 options** ranked by TOPSIS score

---

## 📈 Results Display

### 1. 🎯 Gợi Ý Chính (Top Recommendation)
Shows the single best option with:
- Company name
- ICC package
- Cost ($)
- TOPSIS score
- Confidence level
- Category

### 2. 🏆 Top 3 Gợi Ý Hàng Đầu
Three premium cards with:
- 🥇 Gold medal for #1 (with gold-pulse animation)
- 🥈 Silver medal for #2
- 🥉 Bronze medal for #3
- Full metrics for each

### 3. 📋 Bảng Xếp Hạng Đầy Đủ
Complete ranking of all 15 options with:
- Rank (1-15)
- Company name
- ICC Package
- Category
- Cost
- TOPSIS Score
- Confidence

### 4. ⚠️ Phân Tích Rủi Ro Tài Chính
Risk metrics interpretation:
- **VaR 95%**: Value at Risk at 95% confidence level
- **CVaR 95%**: Conditional Value at Risk (tail loss)
- **Assessment**: Low/Medium/High risk evaluation

### 5. 📊 Phân Tích Chi Tiết & Biểu Đồ
8 interactive charts:
1. **Trọng số tiêu chí** - Pie chart of criteria weights
2. **Bản đồ Chi phí - Điểm TOPSIS** - Cost vs score scatter plot
3. **Top 5 Phương Án Được Chọn** - Bar chart of top 5
4. **Dự Báo Rủi Ro (ARIMA Trend)** - Time series forecast
5. **So Sánh Theo Loại Công Ty** - Company comparison
6. **Mức Độ Không Chắc Chắn (Fuzzy AHP)** - Uncertainty visualization
7. **Phân Tích Độ Nhạy (Spider)** - Sensitivity analysis
8. **Radar Độ Tin Cậy Mô Hình** - Model confidence radar

### 6. 🌀 Phân Tích Fuzzy AHP (If Enabled)
If Fuzzy AHP is enabled:
- Fuzzy membership functions table
- Most uncertain criterion identification
- Fuzzy uncertainty visualization chart

### 7. 📥 Xuất Báo Cáo (Export Options)
- **📄 Xuất PDF** - Download PDF report
- **📊 Xuất Excel** - Download Excel spreadsheet
- **🔄 Phân Tích Lại** - Reset and analyze again

---

## 🎨 Profile Explanation

### 💰 Tiết kiệm chi phí (Cost-focused)
**Best for:** Budget-conscious logistics companies
- **C1 Premium**: 35% (highest weight)
- Focus: Minimize insurance costs
- Recommended for: Standard cargo

### ⚖️ Cân bằng (Balanced)
**Best for:** General purpose coverage
- All criteria: ~17-20% weight
- Focus: Balance cost and protection
- Recommended for: Mixed cargo types

### 🛡️ An toàn tối đa (Safety-focused)
**Best for:** High-value or sensitive cargo
- **C3 Loss ratio**: 25%
- **C4 ICC support**: 25%
- Focus: Maximum protection
- Recommended for: Valuable/fragile cargo

---

## 📄 Export Formats

### PDF Report Includes
- Title and metadata
- Selected priority profile
- Top recommendation details
- Top 10 options table
- Risk assessment
- Confidence metrics

### Excel Spreadsheet Includes
- **Sheet 1 (Kết quả)**: All 15 options with full metrics
- **Sheet 2 (Trọng số)**: Criteria weights used
- **Sheet 3 (Rủi ro)**: VaR/CVaR risk metrics

---

## 🧪 Testing the Application

### Run Integration Tests
```powershell
python test_integration.py
```

Expected output:
```
✅ ALL TESTS PASSED - Refactoring is complete and functional!
```

### Manual Testing Checklist
- [ ] Header displays RC logo correctly
- [ ] Sidebar inputs accept all values
- [ ] Analysis button triggers calculation
- [ ] Top recommendation card displays correctly
- [ ] All 8 charts render without errors
- [ ] PDF export works
- [ ] Excel export works
- [ ] Theme is green (#00e676, #00ff99, #00bfa5)

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Solution**: Install requirements
```powershell
pip install -r requirements.txt
```

### Issue: "statsmodels not found"
**Solution**: Optional dependency for ARIMA. The app will fallback to linear trend.
```powershell
pip install statsmodels
```

### Issue: "Port 8501 already in use"
**Solution**: Kill existing process or use different port
```powershell
streamlit run app/main.py --server.port 8502
```

### Issue: Charts not rendering
**Solution**: Ensure Plotly is installed
```powershell
pip install plotly
```

### Issue: Circular import warning
**Solution**: Normal in test environment, not a runtime issue. Doesn't affect functionality.

---

## 📚 Project Files

### Key Files to Know
- `app/main.py` - Application entry point
- `app/pages/analysis.py` - Main analysis page logic
- `core/mcdm.py` - TOPSIS algorithm and analyzer
- `config/constants.py` - All constants and profiles
- `ui/components.py` - Streamlit UI components
- `ui/charts.py` - Plotly chart factory
- `data/historical_climate.csv` - Historical risk data
- `data/company_data.csv` - Company information

### Documentation Files
- `FINAL_STATUS_REPORT.md` - Complete refactoring report
- `REFACTORING_COMPLETE.md` - Feature inventory
- `guide.txt` - Vietnamese documentation (29 files)
- `README.md` - Project overview

---

## 🔧 Advanced Configuration

### Streamlit Configuration
Located in `.streamlit/config.toml`:
- Page theme
- Layout settings
- Caching configuration

### Environment Variables
Set custom settings via `.env` file (if using python-dotenv)

### Data Files
- CSV format for historical climate data
- CSV format for company metrics
- Can be updated with new routes or companies

---

## 📖 Documentation

For detailed information, see:
- **FINAL_STATUS_REPORT.md** - Complete refactoring details
- **REFACTORING_COMPLETE.md** - Features and architecture
- **guide.txt** - Vietnamese file descriptions

---

## ✅ Checklist Before Deployment

- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] Integration tests pass (`python test_integration.py`)
- [ ] Application starts without errors (`python run.py`)
- [ ] All 8 charts render correctly
- [ ] PDF export works
- [ ] Excel export works
- [ ] Theme displays correctly (green colors)
- [ ] Vietnamese labels display properly
- [ ] Analysis completes in < 5 seconds

---

## 🎓 Learning Resources

### Understanding the Analysis
1. **TOPSIS**: Multi-criteria ranking method
2. **Fuzzy AHP**: Handles uncertainty in weights
3. **Monte Carlo**: Risk simulation via random sampling
4. **VaR/CVaR**: Financial risk metrics

### Understanding the Code
1. Core logic: `core/mcdm.py`
2. UI rendering: `app/pages/analysis.py`
3. Data processing: `core/data.py`
4. Charts: `ui/charts.py`

---

## 📞 Support

For issues or questions:
1. Check FINAL_STATUS_REPORT.md for detailed information
2. Review error messages in terminal output
3. Run test_integration.py to diagnose issues
4. Check .streamlit/config.toml for configuration issues

---

**RISKCAST v5.5 Enterprise Edition**  
*Streamlit + Python 3.13*  
*Production Ready* ✅
