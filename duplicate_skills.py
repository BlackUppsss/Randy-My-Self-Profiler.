import sys

file_path = 'index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the start and end of skills-container and inline-nav-box
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'id="skills-container"' in line:
        start_idx = i
    if '<div class="snap-section min-h-screen flex items-center justify-center p-8" id="section-experience">' in line:
        end_idx = i
        break

# The block to duplicate ends at the closing </div> of inline-nav-box which is around line 1477
inline_nav_start = -1
for i in range(start_idx, end_idx):
    if 'class="inline-nav-box' in lines[i]:
        inline_nav_start = i
        break

# Find where inline-nav-box ends
nav_end_idx = -1
div_count = 0
for i in range(inline_nav_start, end_idx):
    div_count += lines[i].count('<div') - lines[i].count('</div')
    if div_count == 0:
        nav_end_idx = i
        break

# Now duplicate from start_idx to nav_end_idx inclusive
duplicated_block = lines[start_idx:nav_end_idx+1]

mobile_section = [
    '\n    <!-- MOBILE TECHNICAL SKILLS SECTION -->\n',
    '    <div class="snap-section min-h-screen flex md:hidden items-center justify-center p-8" id="section-skills-mobile">\n',
    '        <div class="max-w-6xl mx-auto w-full">\n',
    '            <h2 class="text-4xl md:text-6xl font-black text-white text-shadow-gold text-center mb-8" style="animation: float-1 3s ease-in-out infinite;">\n',
    '                Technical Skills\n',
    '            </h2>\n',
    '            <div class="pixel-corners bg-white/5 backdrop-blur-sm p-4 sm:p-8 flex flex-col justify-between" style="animation: float-3 3.5s ease-in-out infinite;">\n'
]
# replace ids in duplicated block to avoid duplicates
for i in range(len(duplicated_block)):
    duplicated_block[i] = duplicated_block[i].replace('id="skills-container"', 'id="skills-container-mobile"')
    # don't remove fab-highlight yet, we will handle that in js

mobile_section.extend(duplicated_block)
mobile_section.extend([
    '            </div>\n',
    '        </div>\n',
    '    </div>\n\n'
])

# Insert right before end_idx
lines = lines[:end_idx] + mobile_section + lines[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Successfully duplicated Technical Skills for mobile.')
