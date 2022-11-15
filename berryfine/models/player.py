from sqlalchemy import Column, String, Boolean, Integer, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_mixin, declared_attr

Base = declarative_base()


class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)


@declarative_mixin
class CareerStatsMixin:
    @declared_attr
    def player_id(cls):
        return Column(Integer, ForeignKey("player.id"), primary_key=True)

    league_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, primary_key=True)
    cp = Column(Integer, nullable=False)
    gs = Column(Integer, nullable=False)
    mins = Column(Float, nullable=False)
    fgm = Column(Integer, nullable=False)
    fga = Column(Integer, nullable=False)
    fg_pct = Column(Float, nullable=False)
    fg3m = Column(Integer, nullable=False)
    fg3_pct = Column(Float, nullable=False)
    ftm = Column(Integer, nullable=False)
    ft_pct = Column(Float, nullable=False)
    oreb = Column(Integer, nullable=False)
    dreb = Column(Integer, nullable=False)
    reb = Column(Integer, nullable=False)
    ast = Column(Integer, nullable=False)
    stl = Column(Integer, nullable=False)
    blk = Column(Integer, nullable=False)
    tov = Column(Integer, nullable=False)
    pf = Column(Integer, nullable=False)
    pts = Column(Integer, nullable=False)


@declarative_mixin
class SeasonStatsMixin(CareerStatsMixin):
    @declared_attr
    def team_id(cls):
        return Column(String, ForeignKey("team.id"), primary_key=True)

    season_id = Column(Date, primary_key=True)
    team_abbreviation = Column(String, nullable=False)
    player_age = Column(Integer, nullable=False)


@declarative_mixin
class SeasonRankingStatsMixin(object):
    @declared_attr
    def player_id(cls):
        return Column(Integer, ForeignKey("player.id"), primary_key=True)

    @declared_attr
    def team_id(cls):
        return Column(String, ForeignKey("team.id"), primary_key=True)

    league_id = Column(Integer, primary_key=True)
    team_abbreviation = Column(String, nullable=False)
    player_age = Column(Integer, nullable=True)
    gp = Column(Integer)
    gs = Column(Integer)
    rank_min = Column(Integer)
    rank_fgm = Column(Integer)
    rank_fg_pct = Column(Integer)
    rank_fg3m = Column(Integer)
    rank_fg3a = Column(Integer)
    rank_fg3_pct = Column(Integer)
    rank_ftm = Column(Integer)
    rank_fta = Column(Integer)
    rank_ft_pct = Column(Integer)
    rank_oreb = Column(Integer)
    rank_dreb = Column(Integer)
    rank_reb = Column(Integer)
    rank_ast = Column(Integer)
    rank_stl = Column(Integer)
    rank_blk = Column(Integer)
    rank_tov = Column(Integer)
    rank_pts = Column(Integer)
    rank_eff = Column(Integer)


class CareerTotalsAllStarSeason(Base, CareerStatsMixin):
    __tablename__ = "player_career_totals_allstar_season"


class CareerTotalsPostSeason(Base, CareerStatsMixin):
    __tablename__ = "player_career_totals_post_season"


class CareerTotalsRegularSeason(Base, CareerStatsMixin):
    __tablename__ = "player_career_totals_regular_season"


class CareerTotalsCollegeSeason(Base, CareerStatsMixin):
    __tablename__ = "player_career_totals_college_season"


class SeasonTotalsRegularSeason(Base, SeasonStatsMixin):
    __tablename__ = "player_season_totals_regular_season"


class SeasonTotalsPostSeason(Base, SeasonStatsMixin):
    __tablename__ = "player_season_totals_post_season"


class SeasonTotalsCollegeSeason(Base, SeasonStatsMixin):
    __tablename__ = "player_season_totals_college_season"


class SeasonRankingsRegularSeason(Base, SeasonRankingStatsMixin):
    __tablename__ = "player_season_rankings_regular_season"


class SeasonRankingsPostSeason(Base, SeasonRankingStatsMixin):
    __tablename__ = "player_season_rankings_post_season"
