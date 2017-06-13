module Reading
	class Generator < Jekyll::Generator
		def generate(site)
			
			# percentage of default fonr size
			size_min = 80
			size_max = 250
			
			
			tagpage = site.pages.detect {|page| page.name == 'tags.html'}
			
			alltags = Hash.new { |hsh, key| hsh[key] = Array.new }
			tagcloud = Hash.new { |hsh, key| hsh[key] = Array.new }
			
			# collect all tags and corresponding pages/posts
			# pages
			site.pages.each do |post|
				if post.data["tags"]
					post.data["tags"].each do |tag|
						alltags[tag] << post
					end
				end
			end
			# posts
			site.posts.docs.each do |post|
				if post.data["tags"]
					post.data["tags"].each do |tag|
						alltags[tag] << post
					end
				end
			end
			
			# find min/max
			min = 10000
			max = 0
			alltags.keys.each do |t|
				if min > alltags[t].size
					min = alltags[t].size
				end
				if max < alltags[t].size
					max = alltags[t].size
				end
			end
			
			# scale tags
			alltags.keys.each do |tag|
				size = (Math.log(alltags[tag].size) - Math.log(min))/(Math.log(max) - Math.log(min))
				size = size_min + ((size_max - size_min) * size).to_f
				size = sprintf("%.1f", size)
				tagcloud[tag] = size
			end
			
			# sort by tag name
			tagcloud = Hash[ tagcloud.sort_by { |key, val| key } ]
			alltags = Hash[ alltags.sort_by { |key, val| key } ]
			
			# submit the information to the tagpage..
			tagpage.data["alltags"] = alltags
			tagpage.data["tagcloud"] = tagcloud
		end
	end
end

