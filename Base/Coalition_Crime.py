# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 13:41:36 2018

@author: zli34
"""

from Base.Coalition import Coalition
import logging


# from environ_config import environ as environ

class Coalition_Crime(Coalition):
    """A subclass of Coalition
    Attributes:
        of_type: The type of the coalition
        members: List of agents in the coalition
        uid: unique ID for coalition
        network: The original network id where the coalition is nested in 
        resources: The amount of each asset the coalition has
        history_self, history_others: The coalition's memory of history of itself and others
        policy: The coalition's policy
        competitors: The coalition's competitors

        location
        combined_crime_propensity
    """

    def __init__(self, uid, environment):
        """
        :param uid: The unique id for the coalition.
        :param environment: The environment the coalition is in.
        """
        super().__init__(uid, environment)
        self.combined_crime_propensity = 0

    def __str__(self):
        return "Illicit Network " + str(self.uid)

    def add_member(self, agent):
        """Adds a member to the list of members.
        :param: The agent that will be added as a member of the coalition."""
        # assert(type(agent) == Criminal)

        logging.info(str(self) + " is getting " + str(agent))
        self.members.append(agent)
        self.combined_crime_propensity += agent.crime_propensity
        agent.network = self
        return True

    def remove_member(self, agent):
        """Removes an agent from a network.
        :param agent: The agent that will be removed from the coalition."""
        logging.info(str(agent) + " is leaving " + str(self))
        # assert(type(agent) is Criminal)
        self.members.remove(agent)
        self.combined_crime_propensity -= agent.crime_propensity
        agent.network = None

        # Dissolve coalition if there are 1 or less members
        if len(self.members) <= 1:
            for coalition in self.environment.criminal_coalitions:
                logging.info(str(coalition))
            self.remove_coalition()

    def remove_coalition(self):
        """Remove this coalition forever."""
        # Delete this coalition
        self.environment.remove_coalition(self)

    def merge(self, other_coalition):
        """Merge another coalition's members into this coalition.
        :param other_coalition: Another coalition the coalition will merge with."""
        for criminal in other_coalition.members:
            self.add_member(criminal)
            assert(criminal.network is self)

        # Delete the other coalition
        logging.info(str(self) + " is absorbing " + str(other_coalition))
        other_coalition.remove_coalition()

        return True



