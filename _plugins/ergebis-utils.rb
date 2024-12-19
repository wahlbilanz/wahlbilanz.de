module ErgebnisUtils
    def ergebnis_max(ergebnis)
        if ergebnis.has_key?("gesamt")
            ergebnis.delete("gesamt")
        end
        return ergebnis.values.max
    end
  end
  
  Liquid::Template.register_filter(ErgebnisUtils)
  