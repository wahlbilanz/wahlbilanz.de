module DatumDisplay
    def datum_display(datum)
        re = /^(\d?\d)\. ?([A-Z][a-zä]+) (\d\d\d\d)/
        if (defined?(datum)).nil?
            return ""
        end
        md = re.match(datum)
        if md
            month_number = ""
            case md[2].downcase
            when "januar"
              month_number = "01"
            when "februar"
              month_number = "02"
            when "märz"
              month_number = "03"
            when "april"
              month_number = "04"
            when "mai"
              month_number = "05"
            when "juni"
              month_number = "06"
            when "juli"
              month_number = "07"
            when "august"
              month_number = "08"
            when "september"
              month_number = "09"
            when "oktober"
              month_number = "10"
            when "november"
              month_number = "11"
            when "dezember"
              month_number = "12"
            else
              month_number = ""
            end
            
            if month_number.length == 2
                return "Datum: <time datetime=\"#{md[3]}-#{month_number}-#{md[1].rjust(2, '0')}\">#{datum}</time>"
            end

            # return "Datum matched! " + md[1] + md[2] + md[3]
        end
        return "Datum: <strong>#{datum}</strong>"
    end
  end
  
  Liquid::Template.register_filter(DatumDisplay)