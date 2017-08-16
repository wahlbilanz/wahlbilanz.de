module PartyNameFixer
  def party_name(name)
    case name
		when "cdu/csu"
			return "CDU/CSU"
		when "die.linke"
			return "Die Linke"
		when "gruenen"
			return "Bündnis 90/Die Grünen"
		when "spd"
			return "SPD"
		when "fraktionslos"
			return "Fraktionslos"
		end
		return name
  end
end

Liquid::Template.register_filter(PartyNameFixer)
