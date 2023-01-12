"""
Template for BioSim class.
"""
import random

from biosim.model.Fauna import Herbivore, Carnivore
from biosim.model.Rossumoya import Rossumoya
from biosim.model.UnitArea import UnitArea


# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2023 Hans Ekkehard Plesser / NMBU


class BioSim:
    """
    Top-level interface to BioSim package.
    """

    def __init__(self,
                 island_map,
                 ini_pop,
                 seed,
                 vis_years=1,
                 ymax_animals=None,
                 cmax_animals=None,
                 hist_specs=None,
                 img_years=None,
                 img_dir=None,
                 img_base=None,
                 img_fmt='png',
                 log_file=None):
        """
        Parameters
        ----------
        island_map : str
            Multi-line string specifying island geography
        ini_pop : list
            List of dictionaries specifying initial population
        seed : int
            Integer used as random number seed
        vis_years : int
            Years between visualization updates (if 0, disable graphics)
        ymax_animals : int
            Number specifying y-axis limit for graph showing animal numbers
        cmax_animals : dict
            Color-scale limits for animal densities, see below
        hist_specs : dict
            Specifications for histograms, see below
        img_years : int
            Years between visualizations saved to files (default: `vis_years`)
        img_dir : str
            Path to directory for figures
        img_base : str
            Beginning of file name for figures
        img_fmt : str
            File type for figures, e.g. 'png' or 'pdf'
        log_file : str
            If given, write animal counts to this file

        Notes
        -----
        - If `ymax_animals` is None, the y-axis limit should be adjusted automatically.
        - If `cmax_animals` is None, sensible, fixed default values should be used.
        - `cmax_animals` is a dict mapping species names to numbers, e.g.,

          .. code:: python

             {'Herbivore': 50, 'Carnivore': 20}

        - `hist_specs` is a dictionary with one entry per property for which a histogram
          shall be shown. For each property, a dictionary providing the maximum value
          and the bin width must be given, e.g.,

          .. code:: python

             {'weight': {'max': 80, 'delta': 2},
              'fitness': {'max': 1.0, 'delta': 0.05}}

          Permitted properties are 'weight', 'age', 'fitness'.
        - If `img_dir` is None, no figures are written to file.
        - Filenames are formed as

          .. code:: python

             Path(img_dir) / f'{img_base}_{img_number:05d}.{img_fmt}'

          where `img_number` are consecutive image numbers starting from 0.

        - `img_dir` and `img_base` must either be both None or both strings.
        """
        random.seed(seed)
        self._make_island(island_map)
        self._populate_island(ini_pop)
        print(self._island)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        Parameters
        ----------
        species : str
            Name of species for which parameters shall be set.
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        Parameters
        ----------
        landscape : str
            Code letter for landscape
        params : dict
            New parameter values

        Raises
        ------
        ValueError
            If invalid parameter values are passed.
        """

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        Parameters
        ----------
        num_years : int
            Number of years to simulate
        """
        print("Year\tHerbivore Count")
        for year in range(num_years):
            print(f"{year}\t{Herbivore.count()}")
            for row in self._island.cells:
                for cell in row:
                    BioSim._make_babies(cell)
                    BioSim._eat(cell)
                    BioSim._wander_away(cell, self._island.cells)
                    BioSim._grow_old(cell)
                    BioSim._get_thin(cell)
                    BioSim._meet_your_maker(cell)

    @staticmethod
    def _make_babies(cell):
        no_herbs = len(cell.herbs)
        babies = []
        for herb in cell.herbs:
            baby = herb.procreate(no_herbs)
            if baby is not None:
                babies.append(baby)
        if babies:
            cell.add_herbs(babies)

    @staticmethod
    def _eat(cell):
        remaining_fodder = cell.geo.params.f_max
        herb_indices = [*range(len(cell.herbs))]
        random.shuffle(herb_indices)
        for index in herb_indices:
            if remaining_fodder <= 0:
                break
            remaining_fodder = cell.herbs[index].feed_and_gain_weight(remaining_fodder)

    @staticmethod
    def _grow_old(cell):
        [herb.get_older() for herb in cell.herbs]

    @staticmethod
    def _get_thin(cell):
        [herb.lose_weight() for herb in cell.herbs]

    @staticmethod
    def _meet_your_maker(cell):
        cell._herbs = [herb for herb in cell.herbs if not herb.maybe_die()]

    @staticmethod
    def _wander_away(cell, cells):
        # TODO migration
        pass

    def add_population(self, population):
        """
        Add a population to the island

        Parameters
        ----------
        population : List of dictionaries
            See BioSim Task Description, Sec 3.3.3 for details.
        """

    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""

    def _make_island(self, island_map):
        if island_map is None:
            raise ValueError("No Island")
        island_cells = []
        island_cells.extend(
            [UnitArea((r + 1, c + 1), value) for c, value in enumerate(rows)]
            for r, rows in enumerate(island_map.splitlines())
        )
        self._island = Rossumoya(island_cells)

    def _populate_island(self, population: [{}]):
        if population is None:
            raise ValueError("No Input population.")

        Herbivore().reset_count()
        Carnivore().reset_count()

        for cell_info in population:
            row, col = cell_info.get("loc")
            unit_area: UnitArea = self._island.cells[row - 1][col - 1]
            for pop in cell_info.get("pop"):
                match pop.get("species"):
                    case "Herbivore":
                        unit_area.add_herb(Herbivore(pop.get("age"), pop.get("weight")))
                    case "Carnivore":
                        unit_area.add_carn(Carnivore(pop.get("age"), pop.get("weight")))
                    case _:
                        raise ValueError("Unknown species.")
