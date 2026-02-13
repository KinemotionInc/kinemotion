---
title: Sport-Specific Athlete Profiles Research 2026-02
type: note
permalink: biomechanics/sport-specific-athlete-profiles-research-2026-02
tags:
- normative-data
- athlete-profiles
- sport-specific
- research
- phase-2
---

# Sport-Specific Athlete Profiles Research

**Date:** 2026-02-12
**Status:** Research Phase - Implementation Planned for Phase 2

## Research Question

Should Kinemotion implement sport-specific athlete profiles instead of (or in addition to) training-level profiles?

## Answer: YES - There is substantial 2024-2025 research

### Key Finding

Sport-specific differences in jump performance are **statistically significant**. Different sports emphasize different aspects of the stretch-shortening cycle (SSC).

## Research Sources
### 1. Basketball-Specific Research
- **Source:** IUSCA Journal 2024-2025
- **Study:** "Unlocking Basketball Athletic Performance"
- **Sample:** NCAA Division-I Power Five Men's Basketball (7 universities: Kentucky, Tennessee, Alabama, Purdue, Louisville, Mississippi State)
- **Metrics:** CMJ and CMJ-Rebound (CMJ-RE) normative values
- **Link:** https://journal.iusca.org/index.php/Journal/article/view/354

### 2. Soccer-Specific Research
- **Source:** Journal of Sports Sciences 2025
- **Study:** "Normative data and objective benchmarks for selected force plate tests for professional and youth soccer players in the English Football League"
- **Authors:** Badby, Comfort, Ripley, et al.
- **Coverage:** Professional AND youth specific norms
- **DOI:** 10.1080/02640414.2025.2523671

### 3. Rugby Union-Specific Research ⭐

#### Professional/Elite Level
- **Source:** Movement & Sport Sciences 2021
- **Study:** "Position-specific countermovement jump characteristics of elite Women's Rugby World Cup 2017 athletes"
- **Finding:** Position-specific CMJ differences in elite women's rugby union
- **DOI:** 10.1051/sm/2021013
- **Link:** https://www.mov-sport-sciences.org/articles/sm/full_html/2021/03/sm200080/sm200080.html

- **Source:** Swansea University 2021
- **Study:** "International Female Rugby Union Players' Anthropometric and Physical Performance Characteristics: A Five-Year Longitudinal Analysis by Individual Positional Groups"
- **Authors:** Woodhouse, Tallent, Patterson, Waldron
- **Coverage:** International female players, 5-year longitudinal, position-specific
- **Link:** https://cronfa.swan.ac.uk/Record/cronfa58503

#### Age Grade/Youth Level (Extensive Normative Data)
- **Source:** PLOS ONE 2020 (Systematic Review)
- **Study:** "Testing methods and physical qualities of male age grade rugby union players: a systematic review"
- **Authors:** Owen, Till, Weakley, Jones
- **Coverage:** 42 studies, age-grade (≤U20) male rugby union players
- **Metrics:** CMJ height, CMJ peak power, by position (forwards vs backs) and age group
- **DOI:** 10.1371/journal.pone.0233796
- **Link:** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0233796
- **Normative Data Figure:** https://plos.figshare.com/articles/figure/12427382

- **Source:** Sports Medicine Open 2020
- **Study:** "Applied Sport Science for Male Age-Grade Rugby Union in England"
- **Authors:** Till, Weakley, Read, et al.
- **Coverage:** Comprehensive review of age-grade rugby union physical qualities
- **Link:** https://sportsmedicine-open.springeropen.com/articles/10.1186/s40798-020-0236-6

- **Source:** European Journal of Sport Science 2022
- **Study:** "A multidimensional approach to identifying the physical qualities of male English regional academy rugby union players; considerations of position, chronological age, relative age and maturation"
- **Authors:** Owen, Till, Phibbs, Read, Weakley, et al.
- **Coverage:** Regional academy players, position and age-specific
- **Link:** https://e-space.mmu.ac.uk/628902

#### Key Rugby Union Jump Pattern Insights
- **Position differences:** Backs typically show higher jump heights than forwards
- **Age progression:** Clear CMJ height and power progression across age groups (U16 → U18 → U20)
- **Specialized testing:** CMJ peak power is a key discriminating metric for rugby union

### 4. Rugby League (Related Context)
- **Source:** MDPI Sensors 2022
- **Study:** "Force Plate-Derived Countermovement Jump Normative Data and Benchmarks for Professional Rugby League Players"
- **Authors:** McMahon, Ripley, Comfort
- **Note:** Rugby League (not Union), but provides useful context for collision sport athletes
- **DOI:** 10.3390/s22228669

### 5. Cross-Sport Comparison Study
- **Source:** PubMed 2025
- **Study:** "Sport-Specific Differences in Vertical Jump Force-Time Metrics Between Professional Female Volleyball, Basketball, and Handball Players"
- **Finding:** Statistically significant differences between sports
- **Implication:** Different jumping patterns per sport matter
- **Link:** https://pubmed.ncbi.nlm.nih.gov/40030122/

### 6. Commercial Data Sources
- **Output Sports (2023):** "Normative Data in Jumps Training" - thousands of athletes with sport-specific breakdowns
- **GymAware (2025):** RSI normative charts with sport considerations
### 1. Basketball-Specific Research
- **Source:** IUSCA Journal 2024-2025
- **Study:** "Unlocking Basketball Athletic Performance"
- **Sample:** NCAA Division-I Power Five Men's Basketball (7 universities: Kentucky, Tennessee, Alabama, Purdue, Louisville, Mississippi State)
- **Metrics:** CMJ and CMJ-Rebound (CMJ-RE) normative values
- **Link:** https://journal.iusca.org/index.php/Journal/article/view/354

### 2. Soccer-Specific Research
- **Source:** Journal of Sports Sciences 2025
- **Study:** "Normative data and objective benchmarks for selected force plate tests for professional and youth soccer players in the English Football League"
- **Authors:** Badby, Comfort, Ripley, et al.
- **Coverage:** Professional AND youth specific norms
- **DOI:** 10.1080/02640414.2025.2523671

### 3. Cross-Sport Comparison Study
- **Source:** PubMed 2025
- **Study:** "Sport-Specific Differences in Vertical Jump Force-Time Metrics Between Professional Female Volleyball, Basketball, and Handball Players"
- **Finding:** Statistically significant differences between sports
- **Implication:** Different jumping patterns per sport matter
- **Link:** https://pubmed.ncbi.nlm.nih.gov/40030122/

### 4. Commercial Data Sources
- **Output Sports (2023):** "Normative Data in Jumps Training" - thousands of athletes with sport-specific breakdowns
- **GymAware (2025):** RSI normative charts with sport considerations

## Sport-Specific Jump Patterns
| Sport | Jump Pattern | Key Emphasis |
|-------|--------------|--------------|
| **Basketball** | Multiple rebounds, vertical jumps | CMJ-RE, reactive strength |
| **Volleyball** | Approach jumps (spike/block) | Eccentric loading, jump height |
| **Soccer** | Single-leg dominance, cutting | Asymmetry, reactive strength |
| **Track & Field** | Sprint starts, jumping events | Power output, force-velocity |
| **Handball** | Overhead throwing, blocking | Upper-lower body coordination |
| **Rugby Union** ⭐ | Collision sport, scrums, lineouts | Position-specific (backs > forwards), CMJ peak power, age-grade progression |
| **Rugby League** | Collision sport, play-the-ball | Forwards vs backs differences, reactive strength |
## Implementation Architecture

### Phase 1 (Current - MVP)
- **Keep training-level profiles** (UNTRAINED → ELITE)
- Works across all sports
- Simpler implementation
- Lower maintenance burden

### Phase 2 (Market-Driven)
Add optional sport parameter:

```python
# New enum in core/validation.py
class Sport(Enum):
    BASKETBALL = "basketball"
    VOLLEYBALL = "volleyball"
    SOCCER = "soccer"
    TRACK_FIELD = "track_field"
    HANDBALL = "handball"
    MULTI_SPORT = "multi_sport"  # default
```

**Files to modify:**
1. `src/kinemotion/core/validation.py` - Add Sport enum
2. `src/kinemotion/core/demographics.py` - Add sport field
3. `*/validation_bounds.py` - Add sport-specific bounds for CMJ, DJ, SJ
4. `backend/src/kinemotion_backend/services/interpretation_service.py` - Sport-specific coaching insights
5. `frontend/src/` - Add sport selector to demographics form

### Phase 3 (Data Flywheel)
- Build sport-specific database from collected user data
- Refine norms over time
- **Competitive advantage:** proprietary sport-specific dataset

## Strategic Considerations

### Pros
- More accurate normative comparisons
- Better coaching insights
- Competitive differentiation

### Cons
- Higher implementation complexity
- More research/maintenance burden
- Fragmented user experience (more onboarding questions)

## Recommendation

**MVP-first alignment:** The current training-level approach is appropriate for MVP because:
1. Universal applicability across sports
2. Simpler user onboarding
3. Lower development cost
4. Can be enhanced based on market feedback

**Phase 2 trigger:** Customer feedback on which sports coaches actually want.

## Sources

- IUSCA Basketball Norms: https://journal.iusca.org/index.php/Journal/article/view/354
- Soccer Norms: https://doi.org/10.1080/02640414.2025.2523671
- PubMed Cross-Sport Study: https://pubmed.ncbi.nlm.nih.gov/40030122/


## ```python
# New enum in core/validation.py
class Sport(Enum):
    BASKETBALL = "basketball"
    VOLLEYBALL = "volleyball"
    SOCCER = "soccer"
    TRACK_FIELD = "track_field"
    HANDBALL = "handball"
    MULTI_SPORT = "multi_sport"  # default
```
```python
# New enum in core/validation.py
class Sport(Enum):
    BASKETBALL = "basketball"
    VOLLEYBALL = "volleyball"
    SOCCER = "soccer"
    RUGBY_UNION = "rugby_union"      # ⭐ Extensive age-grade and position data available
    RUGBY_LEAGUE = "rugby_league"    # Related collision sport
    TRACK_FIELD = "track_field"
    HANDBALL = "handball"
    MULTI_SPORT = "multi_sport"      # default
```

## Sources

- IUSCA Basketball Norms: https://journal.iusca.org/index.php/Journal/article/view/354
- Soccer Norms: https://doi.org/10.1080/02640414.2025.2523671
- PubMed Cross-Sport Study: https://pubmed.ncbi.nlm.nih.gov/40030122/
## Sources

- IUSCA Basketball Norms: https://journal.iusca.org/index.php/Journal/article/view/354
- Soccer Norms: https://doi.org/10.1080/02640414.2025.2523671
- PubMed Cross-Sport Study: https://pubmed.ncbi.nlm.nih.gov/40030122/
- **Rugby Union Elite Women (CMJ):** https://doi.org/10.1051/sm/2021013
- **Rugby Union International Women Longitudinal:** https://cronfa.swan.ac.uk/Record/cronfa58503
- **Rugby Union Age Grade Systematic Review:** https://doi.org/10.1371/journal.pone.0233796
- **Rugby Union Age Grade Applied Sport Science:** https://doi.org/10.1186/s40798-020-0236-6
- **Rugby Union Academy Position-Specific:** https://e-space.mmu.ac.uk/628902
