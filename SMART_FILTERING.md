# Smart Location Filtering - Fix for "Only 7 Jobs" Issue

## Problem
After implementing strict location filtering, users were only seeing 7 jobs because:
1. **Too strict filtering** - Removed all jobs without exact location match
2. **Limited India jobs** - Job APIs don't have many India-based positions
3. **Only 3 search queries** - Limited job fetching

## Solution: Smart Filtering

### 1. Adaptive Location Filter ✅
**File:** `pipeline/rank_pipeline.py`

**How it works:**
```python
def rank_jobs(profile, matched_jobs, min_jobs=15):
    # Try strict location filtering first
    strict_filtered = [jobs matching preferred_locations]
    
    if len(strict_filtered) >= 15:
        # Enough jobs found - use strict filter
        return strict_filtered (ranked)
    else:
        # Too few jobs - relax filter, but prioritize location in ranking
        return all_jobs (ranked with higher location weight)
```

**Benefits:**
- ✅ If 15+ India jobs available → Shows only India jobs
- ✅ If <15 India jobs → Shows all jobs, but India jobs ranked higher
- ✅ Users always get sufficient results

### 2. Increased Search Queries ✅
**File:** `main.py`

**Change:**
```python
# Before: 3 queries
for item in search_plan.get("search_queries", [])[:3]:

# After: 5 queries  
for item in search_plan.get("search_queries", [])[:5]:
```

**Benefits:**
- ✅ More diverse job searches
- ✅ Better coverage of role variations
- ✅ More total jobs fetched

### 3. Dynamic Ranking Weights ✅

**Strict Filter Active (15+ matching jobs):**
```python
final_score = 0.75 * semantic + 0.10 * skill + 0.10 * location + 0.05 * seniority
```

**Relaxed Filter (< 15 matching jobs):**
```python
final_score = 0.50 * semantic + 0.10 * skill + 0.35 * location + 0.05 * seniority
                ↓ reduced                        ↑ increased
```

This ensures location-matching jobs appear at the top even when filter is relaxed.

---

## Expected Behavior

### Scenario 1: Plenty of India Jobs (15+)
```
Input: Resume with "India" location
Output: 
  ✅ Location filter applied: 23 jobs match preferred locations
  → Shows only India jobs
  → 20 jobs per page
```

### Scenario 2: Few India Jobs (<15)
```
Input: Resume with "India" location  
Output:
  ⚠️ Only 7 jobs match location filter. Showing all 45 jobs for better selection.
  → Shows all jobs
  → India jobs ranked at top (higher location weight)
  → More choices for user
```

### Scenario 3: No Location Preference
```
Input: Resume without location
Output:
  → Shows all jobs
  → Ranked by semantic similarity
  → No location filtering
```

---

## Console Output

You'll now see helpful messages in the backend logs:

```bash
# When strict filter works:
✅ Location filter applied: 18 jobs match preferred locations

# When relaxed:
⚠️ Only 7 jobs match location filter. Showing all 52 jobs for better selection.
```

---

## Testing

### Test 1: Upload India Resume
```bash
curl -X POST http://localhost:8000/profile/extract \
  -F "file=@test_india_devops_resume.txt"
```

Expected: `"preferred_locations": ["Wayanad, Kerala, India"]`

### Test 2: Check Job Count
Upload resume via UI → Should see **20+ jobs** (not just 7)

### Test 3: Verify Location Ranking
- If 15+ India jobs: Only India jobs shown
- If <15 India jobs: All jobs shown, India jobs at top

---

## Configuration

You can adjust the minimum job threshold:

**File:** `pipeline/rank_pipeline.py`
```python
def rank_jobs(profile, matched_jobs, min_jobs=15):
    #                                    ↑ Change this
    # Default: 15 jobs
    # Increase to 20 for more strict filtering
    # Decrease to 10 for more relaxed filtering
```

---

## Summary

**Before:**
- ❌ Only 7 jobs (too strict)
- ❌ Missing relevant opportunities
- ❌ Poor user experience

**After:**
- ✅ 20+ jobs per page
- ✅ India jobs prioritized when available
- ✅ Fallback to all jobs if needed
- ✅ Smart, adaptive filtering
- ✅ Better user experience

---

## Files Modified

1. ✅ `pipeline/rank_pipeline.py` - Smart filtering logic
2. ✅ `main.py` - Increased query limit to 5

---

## Try It Now!

1. Upload Fahad's resume at `http://localhost:5173/`
2. You should now see **20+ jobs** instead of just 7
3. India jobs will be ranked at the top
4. More choices = better job hunting experience!

**Status:** ✅ **FIXED - Smart filtering active!**
