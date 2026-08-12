# Sources

Accessed 12 August 2026. This package is a broad synthesis of original game-design research,
experimental player-experience studies, named practitioner work, and regulator guidance. It is not
a systematic review and does not establish a universal formula for fun, a universal player-loop
taxonomy, or fixed balance and progression curves. Genre, audience, ability, business model, and
play context materially limit transfer.

## Experience-driven system design

- Hunicke, LeBlanc, and Zubek,
  [“MDA: A Formal Approach to Game Design and Game Research”](https://users.cs.northwestern.edu/~hunicke/MDA.pdf)
  (2004), defines mechanics, runtime dynamics, and intended aesthetic responses; explains the
  opposite designer and player perspectives; and advocates iterative qualitative and quantitative
  analysis. It explicitly rejects a single formula for fun. This supports the experience contract,
  bidirectional trace, and first good/bad pair in `SKILL.md`. MDA is a design lens, not proof that a
  proposed mechanic causes an experience.
- Ryan, Rigby, and Przybylski,
  [“The Motivational Pull of Video Games: A Self-Determination Theory Approach”](https://doi.org/10.1007/s11031-006-9051-8)
  (2006), reports four studies. Studies 1–3 associate autonomy and competence with outcomes in their
  tested games; Study 4's survey of 730 MMO players found autonomy, competence, and relatedness each
  independently related to enjoyment and intended future play. This supports treating motivation as
  multidimensional and audience-dependent, not generalizing relatedness from multiplayer to every
  single-player context, converting needs into a retention recipe, or reading survey association as
  experimental causation.
- Sweetser and Wyeth,
  [“GameFlow: A Model for Evaluating Player Enjoyment in Games”](https://www.valuesatplay.org/wp-content/uploads/2007/09/sweetser.pdf)
  (2005), synthesizes concentration, challenge, skill, control, goals, feedback, immersion, and
  social interaction into heuristic criteria and evaluates two real-time strategy games. It
  supports diagnostic questions about challenge and feedback; its heuristic case evaluation does
  not prove a universal optimum or lift.
- Worch,
  [“Decisions That Matter—Meaningful Choice in Game and Level Design”](https://www.gdcvault.com/play/1020570/Level-Design-in-a-Day)
  (GDC 2014), is a named practitioner treatment connecting choice to motivation, agency, possibility
  space, and level design. It supports checking whether alternatives create material tradeoffs.
  The talk is practitioner guidance, not a controlled comparison, and the package also preserves
  games whose intended experience does not depend on strategic choice.
- Prasertvithyakarn,
  [“Can You Make a Good Game Without Good Play Mechanics?”](https://www.gdcvault.com/play/1025983/Can-You-Make-a-Good)
  (GDC 2019), uses *Final Fantasy XV* examples to argue that games can create value through
  experiences beyond mechanical challenge and strategic choice. It supports rejecting meaningful
  choice as a universal definition of a good game.

## Loops, challenge, balance, and economies

- Brink,
  [“The ‘Turducken’ Method of Game Design and Analysis”](https://www.gdcvault.com/play/1014958/The-Turducken-Method-of-Game)
  (GDC Europe 2011), presents nested micro, progression, and longer experience loops as a practical
  analysis method. The package adopts nested-loop analysis but deliberately replaces the talk's
  compulsion framing with voluntary player action, readable response, and state change.
- Hunicke, LeBlanc, and Zubek's MDA paper also analyzes reinforcing feedback in *Monopoly*, where
  increasing advantage can remove tension and agency for trailing players. It supports inspecting
  reinforcing and balancing relationships rather than assuming either is inherently desirable.
- Schreiber,
  [“A Course About Game Balance”](https://www.gdcvault.com/play/1023349/A-Course-About-Game)
  (GDC 2016), frames balance as a practiced discipline spanning multiple kinds of relationships and
  exercises. Schreiber and Romero's
  [*Game Balance* publisher description and contents](https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577)
  (2021) identify numeric relationships, economies, probability, progression, analytics, and
  metagame systems as distinct balance concerns. These sources support the relationship-first scope
  of the conditional reference, not any unpublished numeric prescription.
- Alexander et al.,
  [“An Investigation of the Effects of Game Difficulty on Player Enjoyment”](https://doi.org/10.1016/j.entcom.2012.09.001)
  (2013), reports an experiment with 90 participants comparing static and dynamic difficulty. Its
  finding that enjoyment related to gaming experience rather than measured ability supports
  audience- and context-specific tuning, not a universal difficulty-selection rule.
- Davidson,
  [“Economic Decision Making in Game Design”](https://gdcvault.com/play/1013861/Economic-Decision-Making-in-Game)
  (GDC Online 2010), is practitioner guidance on loss aversion, mental accounting, diminishing
  sensitivity, sunk costs, and flat-rate bias. It supports evaluating perceived costs and player
  behavior beside mathematical value. Because the talk also addresses monetization optimization,
  regulator sources below govern the package's ethical boundary.

## Ethical engagement and purchases

- The OECD's
  [“Dark Commercial Patterns”](https://doi.org/10.1787/44f5e846-en)
  (Digital Economy Paper 336, 2022) synthesizes evidence that interface practices can steer,
  deceive, coerce, or manipulate consumers and cause financial, privacy, and psychological harms.
  It supports rejecting attention or spending as isolated design objectives.
- The U.S. Federal Trade Commission's
  [“Bringing Dark Patterns to Light”](https://www.ftc.gov/system/files/ftc_gov/pdf/P214800%20Dark%20Patterns%20Report%209.14.2022%20-%20FINAL.pdf)
  (2022) documents hidden costs, unauthorized charges, disguised advertising, obstructed
  cancellation, and children's in-app-purchase patterns. The FTC's
  [final Epic Games order](https://www.ftc.gov/news-events/news/press-releases/2023/03/ftc-finalizes-order-requiring-fortnite-maker-epic-games-pay-245-million-tricking-users-making)
  (2023) describes unwanted charges caused by counterintuitive and inconsistent controls. These
  sources map to the purchase good/bad pair in `SKILL.md`; they are U.S. enforcement materials, not
  a complete global compliance rule.
- The European Commission's
  [consumer-protection notice for online games](https://commission.europa.eu/topics/consumers/consumer-rights-and-complaints/enforcement-consumer-protection/coordinated-actions/social-media-online-games-and-search-engines_en)
  and its
  [2022 letter on paid random content](https://commission.europa.eu/system/files/2023-07/Commission%20letter%20to%20ISFE%20EGDF%20on%20loot%20boxes%20from%20September%202022.pdf)
  address price disclosure, behavioral manipulation, nagging, purchases at critical gameplay
  moments, “free” claims, and direct exhortations to children. They support an explicit
  jurisdiction-review gate rather than encoding one worldwide rule.

## Good/bad pair mapping and limits

- The experience-hypothesis pair applies MDA's experience-driven, iterative analysis and Worch's
  meaningful-choice lens. It does not claim the hypothetical scan mechanic will work.
- The resource-flow pair applies MDA's feedback-system analysis and the system categories in
  Schreiber and Romero. The exact source, sink, cap, and edge-state model is this catalog's
  conservative synthesis for exposing interactions before tuning.
- The purchase pair applies the FTC report and Epic order's documented unwanted-charge and hidden-
  recovery failures.
- The weapon-balance pair applies Schreiber's relationship-based balance scope; equal average
  damage is intentionally presented as insufficient evidence, not as a sourced failed product.
- The currency pair applies MDA's warning that changes cascade through feedback systems and
  Davidson's treatment of perceived economic decisions. No source supplies universal currency
  rates, so the package supplies none.

The GameFlow PDF and some GDC pages provide practitioner frameworks or session overviews rather
than complete experimental records. They are used only for bounded diagnostic guidance. No claim
depends on AAAbench or its upstream packages; those repositories informed topic discovery only.
